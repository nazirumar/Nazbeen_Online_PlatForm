import helpers

from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand


STATICFILES_VENDOR_DIR = getattr(settings,'STATICFILES_VENDOR_DIR')

VENDOR_STATICFILES = {

    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "jquery.min.js": "https://code.jquery.com/jquery-3.6.0.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map",
    # -___________
    "flowbitenpm.min.js":"https://cdn.jsdelivr.net/npm/flowbite@2.5.1/dist/flowbite.min.js",
    
    "cloudinary.min.js": "https://cdnjs.cloudflare.com/ajax/libs/cloudinary-video-player/2.0.5/cld-video-player.min.js",
    "cld-video-player.min.css":"https://cdnjs.cloudflare.com/ajax/libs/cloudinary-video-player/2.0.5/cld-video-player.min.css",
    "cld-video-player.min.js":"https://cdn.jsdelivr.net/npm/cloudinary-video-player@2.1.0/dist/cld-video-player.min.js",
    "htmx.min.js":"https://unpkg.com/htmx.org@2.0.2/dist/htmx.min.js"
    #   __________________
}

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading vendor static files")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helpers.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(
                    self.style.ERROR(f'Failed to download {url}')
                )
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS('Successfully updated all vendor static files.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Some files were not updated.')
            )