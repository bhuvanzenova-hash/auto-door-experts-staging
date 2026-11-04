# Install guide: The Auto Door Experts templates

Built for Elementor 3.34 (free), Royal Elementor Addons and Contact Form 7, which your site already has. About 45 minutes.

**Do this on a staging copy first, with a full backup.** These templates have been checked against the plugin code but have not yet been imported into a real WordPress site, or tested with your IdooraPro theme.

## 1. Upload 4 photos (do this first)

On the **live** site, go to **Media > Add New** and upload the 4 files in `media/`. Nothing on the site changes.

- Do this **in November 2026**. The templates look for them at `/wp-content/uploads/2026/11/`. In a later month, regenerate with `python3 elementor/generate.py --media-month 2026/12`.
- Check this URL opens: https://theautodoorexperts.com.au/wp-content/uploads/2026/11/ind-healthcare.jpg
- If it doesn't, the 4 images import as grey placeholders. You can swap them by hand in Elementor.

## 2. Check one Elementor setting

**Elementor > Settings > Features**: if **Nested Elements** is listed, set it to **Active**. The industry tabs and FAQs need it.

## 3. Paste the CSS

**Appearance > Customize > Additional CSS**: paste all of `global.css` at the end, then **Publish**.

## 4. Create the quote form

**Contact > Add New**, then follow `contact-form-7-setup.txt`.

- The title must be exactly `Auto Door Quote`. The pages find the form by that name.
- The form tab and mail tab are both in that file.
- If the mail tab shows a yellow warning about the **To** field, send a test enquiry before relying on it. `[service]` is how each enquiry reaches the right department.

## 5. Import the templates

**Templates > Saved Templates > Import Templates**: choose `auto-door-templates-import.zip`. It adds all 12 templates at once, and every title starts with `ADE`. If a template is missing afterwards, import its single file from `templates/`.

Use this screen only. These are Elementor templates, so **don't** upload them under **Plugins > Add New > Upload**, **Appearance > Themes > Upload** or **Elementor > Tools > Import/Export**. Those screens expect a different kind of file and will reject the zip.

## 6. Build the pages

For each page: **Edit with Elementor**, delete the old sections, click the folder icon, choose **My Templates**, then **Insert** the matching template.

| Page (URL) | Template |
|---|---|
| Home | ADE Home |
| /emergency-breakdown-service/ | ADE Emergency Breakdown |
| /sales-and-installation/ | ADE Sales & Installation |
| /periodic-maintenance/ | ADE Periodic Maintenance |
| /spare-parts/ | ADE Spare Parts |
| /industries/ (**new page**, create it first) | ADE Industries |
| /about-us/ | ADE About |
| /contact-us/ | ADE Contact |
| /blog/ | ADE Blog |

On each page, under **Page Attributes > Template**, choose **Elementor Full Width**, and turn on **Hide Title**.

## 7. Header, footer and blog articles

Go to **Royal Addons > Theme Builder**. Open the template that is active on your site, delete its contents, and insert:

| Tab | Template |
|---|---|
| Header | ADE Header |
| Footer | ADE Footer |
| Single (Posts) | ADE Single Post |

Keep your existing display conditions. If there is no Single template yet, create one and apply it to all posts.

**Menu:** the header uses your first WordPress menu. In **Appearance > Menus**, put the four services under a `Services` item, and add `Industries`.

## 8. Test before going live

- [ ] Send one enquiry for each of the 4 services, and confirm each reaches the right inbox
- [ ] Links ending in `?service=Maintenance` open the form with that option selected
- [ ] Choosing "Emergency repair" shows the "calling is fastest" message
- [ ] Industry tabs and FAQs open and close
- [ ] Check on a real phone: menu, sticky Call / Quote bar, no sideways scrolling
- [ ] The header stays visible while scrolling
- [ ] Open a blog article: "On this page" list, progress bar, images
- [ ] The hero doors slide open on the homepage

## If something looks wrong

Most likely it's your theme's styles overriding a template. Send me a screenshot and the page URL, and I'll adjust `global.css`.

## How it differs from the preview

- **Icons** are Font Awesome (built into Elementor), so they're slightly heavier than the preview's line icons.
- **Blog topic filters** are left out. Your live categories are placeholder words (aut, cumque, illo...), so they'd need real categories first.
- **Colours and fonts** are set directly on each element rather than through Global Colors, so the pages look right without changing your Site Settings. To change the brand red everywhere, tell me and I'll regenerate.
- **Form messages** (errors and thank-you) are Contact Form 7's own, shown in the form.
