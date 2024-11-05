# Pixieset Gallery Downloader

This script allows you to download images from a Pixieset gallery, organizing them into folders by size and preserving original filenames.

## Prerequisites

- Python 3.6 or higher
- `requests` library (install with `pip install requests`)

## Usage Instructions

1. Run the script: python pixieset_downloader.py
2. When prompted, enter the Pixieset gallery URL. For example: Enter the Pixieset.com URL: https://example.pixieset.com/gallerynamehere/
3. Next, you'll need to find the 'cid' value. Here's how:

a. Open the Pixieset gallery URL in your web browser (Chrome recommended).

b. Press F12 to open Developer Tools.

c. Go to the Network tab in Developer Tools.

d. Reload the webpage.

e. In the Network tab, use the filter feature to search for 'loadphotos'.

f. Click on the 'loadphotos' request.

g. In the Headers view, look for a URL similar to this:
   ```
   https://example.pixieset.com/client/loadphotos/?cuk=gallerynamehere&cid=XXXXXXXX&gs=highlights&page=1
   ```

h. The 'cid' value is the number after `cid=` in this URL (XXXXXXXX in the example above).

4. When the script prompts for the 'cid' value, enter the number you found: Enter the 'cid' value: XXXXXXXX

5. The script will start downloading images, organizing them into folders by size (thumb, small, medium, large, xlarge, xxlarge) within a parent directory named after the photographer, gallery, and current date.

6. Once complete, you'll find a CSV file with image metadata in the parent directory.

## Notes

- This script is for personal use only. Respect copyright and terms of service of Pixieset and the photographer.
- Downloading may take some time depending on the number and size of images in the gallery.
- Ensure you have permission to download the images before using this script.

## Troubleshooting

If you encounter any issues:
- Make sure you're using the correct 'cid' value.
- Check your internet connection.
- Verify that the gallery is accessible in your web browser.

For any other problems, please open an issue in this repository.
