import time
from django.core.management.base import BaseCommand
from IGDReviews.models import Review
from IGDReviews.igdb_api import search_igdb_games


class Command(BaseCommand):
    help = 'Backfill `game_id` for Review objects by searching IGDB for the review.game name.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Do not save changes; only print what would be changed')
        parser.add_argument('--limit', type=int, default=0, help='Maximum number of reviews to process (0 = all)')
        parser.add_argument('--sleep', type=float, default=0.25, help='Seconds to sleep between API calls')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']
        sleep = options['sleep']

        qs = Review.objects.filter(game_id__lte=0).order_by('id')
        total_missing = qs.count()
        if limit > 0:
            qs = qs[:limit]

        self.stdout.write(f'Found {total_missing} reviews with missing game_id. Processing {qs.count()} reviews.')

        updated = 0
        for review in qs:
            name = (review.game or '').strip()
            if not name:
                self.stdout.write(f'Review {review.id}: empty game name, skipping')
                continue

            try:
                results = search_igdb_games(name)
            except Exception as e:
                self.stderr.write(f'Error searching IGDB for "{name}": {e}')
                continue

            match = None
            # Look for case-insensitive exact name match first
            for r in results:
                if 'name' in r and r['name'].strip().lower() == name.lower():
                    match = r
                    break

            # Fallback to first result
            if not match and results:
                match = results[0]

            if match and 'id' in match:
                new_game_id = match['id']
                self.stdout.write(f'Review {review.id}: "{name}" -> game_id {new_game_id} ({match.get("name")})')
                if not dry_run:
                    review.game_id = new_game_id
                    review.save(update_fields=['game_id'])
                    updated += 1
            else:
                self.stdout.write(f'Review {review.id}: No IGDB match found for "{name}"')

            time.sleep(sleep)

        self.stdout.write(self.style.SUCCESS(f'Done. Updated {updated} reviews.'))
