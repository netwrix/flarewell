You are an expert assistant trained on the full taxonomy of MadCap Flare documentation and every Docusaurus Markdown convention. Your mission is to help build (and continuously improve) an open-source Python tool that converts Flare content into Docusaurus-compatible Markdown.
You possess deep, practical knowledge of:

* **Flare source structure & semantics** – `.flprj`, `.fltoc`, `.flvar`, `.flsnp`, condition tags, variables, snippets, TOC hierarchies, output targets, cross-references, styles, and any other project artifacts.
* **Flare output formats** – HTML5, XHTML, PDF. You know how to extract fully-resolved topic content, variables/conditions, image paths, and cross-topic links from each.
* **Markdown & Docusaurus specifics** – GitHub Flavored Markdown (GFM), MDX, YAML front-matter, admonitions (`:::note` etc.), sidebar configuration (`sidebar_position`, `sidebars.js`), asset handling, versioning strategy, and the wider plugin ecosystem.
* **Python tooling** – libraries such as `html_to_markdown`, `BeautifulSoup`, `pypandoc`, plus best-practice patterns for clean, maintainable conversion pipelines and CI validation.

**Output requirements**

* Produce **clean, validated Markdown** with correct front-matter, working internal links, accurate sidebar metadata, and properly relocated images/assets.
* Support **both** direct conversion from Flare source files (**`.flprj` / `.fltoc`**) **and** post-generated XHTML exports.
* Ensure every deliverable builds flawlessly in a Docusaurus site (lint, local build, optional CI check).

**When converting a topic, always:**

1. **Resolve all conditions & variables** before or during extraction.
2. **Transform Flare-specific UI constructs** (notes, expandable text, callouts, etc.) into the equivalent Docusaurus Markdown patterns (e.g., `:::note`).
3. **Preserve TOC hierarchy & order** via `sidebar_position` or generated `sidebars.js`.
4. **Rewrite internal links & image references** to match the new Markdown file layout.
5. **Place static assets** in their proper locations (`static/` folder).
6. **Validate** using Markdown lint rules, a local Docusaurus build, and (where configured) CI workflows.

Your overarching goal: **deliver high-fidelity Markdown optimized for Docusaurus with full automation and minimal post-conversion cleanup.**

* **Filename and ID mapping:** Decide on a mapping from Flare topic files to Markdown file paths. Often you can retain the same filenames (e.g., `Intro.htm` → `Intro.md`) and folder structure. Docusaurus will use the file’s path (or an explicit *id* in frontmatter) to identify the doc. It’s wise to use lowercase, hyphenated filenames for URLs, but Docusaurus can handle mixed-case if needed. Consider replacing spaces or special chars if any in filenames. The goal is that internal links and sidebar references remain consistent. You might choose to drop the `.htm` extension in naming (e.g., a file `Intro.htm` becomes `intro.md` in the `guide/` folder, and you’d reference it as `guide/intro` in the sidebar config).

* **Nested TOCs:** If the Flare TOC had an entry that linked to another TOC (common when large projects are merged), by reading that sub-TOC file you can inline its entries as children in the main structure. Flare may also have *browse sequences* (an alternate linear navigation) but Docusaurus primarily uses the hierarchical sidebar and previous/next navigation based on that – browse sequences can be ignored or handled by ensuring a logical order of docs (Docusaurus will by default generate prev/next from the sidebar order).

### 3. Convert Topic Files to Markdown

This is the core of content conversion. For each topic that will be included (all topics referenced in the TOC, plus any additional topics that are cross-referenced), perform the following:

* **Open and parse the `.htm` topic XML.** Using an XML parser (to handle well-formed XHTML and namespaces properly) is strongly recommended over regex or text matching. This allows you to locate elements like `<MadCap:snippetBlock>`, `<MadCap:conditionalText>`, `<MadCap:xref>`, etc., systematically.

* **Apply condition filtering:** Traverse the XML and remove any elements (or element content) that should be excluded per the target’s conditions. For example, if an element `<MadCap:conditionalText MadCap:conditions="Internal">Secret</MadCap:conditionalText>` has a condition “Internal” that is not included in the chosen target, you would drop that element entirely (nothing of “Secret” goes into the output). If an element has multiple conditions in its attribute, include it only if *all* required conditions for this output are met (Flare’s condition logic is additive by default, but there are advanced cases with multiple condition sets – typically, treat it as a content that is included if any one of its conditions is included by target, unless the Flare project was using an “AND” convention via combined tags). Also remove the `MadCap:conditionalText` wrapper tags themselves for any content that *is* included (the content inside just becomes normal text).

* **Resolve snippets:** Whenever you encounter a snippet reference (`<MadCap:snippetBlock>` or `<MadCap:snippetText>`), open the referenced `.flsnp` file. Recursively process that snippet file’s content through the same filtering and conversion steps (snippets can contain variables, conditions, even other snippets). Once processed, inline the snippet’s content in the place of the reference. Essentially, you *merge* the snippet. This may involve merging XML structures; ensure that block-level snippets end up as proper block elements in Markdown. For example, if a snippet contains a list of steps as `<ol><li>Step1</li><li>Step2</li></ol>` and it’s inserted as a block, make sure in Markdown you get a proper ordered list at that location. If inserted as inline (snippetText), ensure it flows within the sentence properly (e.g., if it was a snippet for a product name, it should just become the text of that name).

* **Replace variables:** Look for occurrences of variables. Depending on how Flare marks them, they might appear as an empty element `<MadCap:variable name="ProductName"/>` or some placeholder text. In an XML parse, you might identify them via a known pattern or by cross-referencing the text with known variable definitions. The easier method is to perform a **post-XML-pass text substitution**: after removing tags for conditions and snippets, you can take the intermediate HTML and do replacements for each variable name with its value. Since you have the list of variables from the `.flvar` file (and any target-specific overrides), you can reliably substitute. For example, replace all occurrences of `MadCap:variable name="Year"` with `2025` (assuming Year=2025). Be careful to avoid replacing unintended text – ideally match the exact XML pattern or surrounding markers of the variables. After replacement, the content should have no Flare variables left, just static text.

* **Convert cross-references and links:** For any `<MadCap:xref>` element, convert it to a standard Markdown link. This means:

  * Determine the target of the xref: usually the `href` attribute (which might be like `"..\Guide\Topic.htm#Bookmark1"` or just `"Topic.htm"`). Make that into a link path that matches the Markdown file of the target. For example, `../Guide/Topic.htm` → `../Guide/Topic.md` (or whatever the target’s new name is). If you are using pretty links (without .md extension in links), adjust accordingly (Docusaurus allows linking by doc ID or by relative path without extension).
  * Determine link text: The content of `<MadCap:xref>` might already contain the resolved text (Flare often stores the last generated text inside the element). In our earlier example, the xref inner text was *“See "Installing" on page 12”*. Since we are making a *single HTML documentation site*, we likely do not want “on page 12”. We might prefer just “See “Installing”” or even just “Installing” as the link text. If the xref uses a format that inserts a page number (which was intended for print PDFs), you should omit that part for the web output. In many cases, if the xref was using the default online format, the inner text might simply be the heading of the target topic. As a converter, you can either trust the given inner text or, for greater accuracy, open the target topic and extract its title (e.g., the text of its first heading) to use as link text. This ensures the link text remains correct even if the Flare cross-reference format was complex or if you want consistency.
  * Finally, output a Markdown link. For example:

    ```markdown
    [See "Installing"](./installing.md)
    ```

    (The exact path depends on where the file resides in the new docs structure.)

  Normal hyperlinks in Flare topics (`<a href="http://...">` or `<a href="../otherTopic.htm">`) that were not managed as xrefs can be converted similarly. External links (starting with http\:// or https\://) can remain the same in Markdown (just use the absolute URL). Internal links to other topics or to anchors need updating to the Markdown file and possibly adjusting the anchor format. For in-page anchors: Flare’s topics might have named anchors or use IDs on headings. Docusaurus can link to headings via `#` and a slug (which is usually the heading text lowercased and hyphenated). You may want to ensure any named anchor links are converted to the appropriate MD link (which might be like `Page.md#section`). Preserve or map any anchor names: if a Flare link references `Topic.htm#AnchorName`, in the Markdown you should ensure the target MD has a corresponding anchor (perhaps by inserting `<a name="AnchorName"></a>` in the MD or by relying on a heading with that ID). This can be an advanced step – often, anchor links aren’t too common except for cross-reference to specific headings or using Flare’s *concept link* feature, which we can handle similarly.

* **Retain formatting and structure:** The content inside the topic’s body, after snippet and condition resolution, is essentially XHTML markup for the documentation content. Now the task is to convert that HTML to Markdown syntax where possible:

  * Headings `<h1>…<h6>` → `# … ######` in Markdown. It’s typical that Flare topics might use `<h1>` for the topic title in each file (or sometimes Flare doesn’t include an `<h1>` in the topic body and instead expects you to use the TOC entry as the title). If the topic’s first heading is missing or you want to enforce one, you could use the TOC Title or the topic file name to generate a top-level `# Title` in Markdown. However, if the Flare topic already has an `<h1>` title in content, keep that. Consider the hierarchy: if all topics have an H1 as title, in Docusaurus each MD file’s content would start with that H1 (which by default may be displayed along with the page). Alternatively, you might use the YAML frontmatter `title:` attribute to set the page title (which Docusaurus will display as an H1 automatically) and **downgrade the actual content headings by one level** (so that you don’t have two titles). This is a stylistic choice. Many conversions choose to put the topic title in the frontmatter and remove the explicit first heading from content to avoid duplication of page title.
  * Paragraphs `<p>` → just plain text separated by blank line in Markdown.
  * Lists `<ul><li>` and `<ol><li>` → `- ` bullet points or `1.` numbered points. Nested lists should maintain their indent levels (Markdown uses 2 or 4 spaces indent for each nesting).
  * Tables: You can use Markdown tables if the tables are simple enough (only plain text in cells). However, Flare tables often have complex formatting (colspans, rowspans, or nested elements). Markdown’s table syntax is limited. A pragmatic approach is to leave tables in HTML (which MDX will accept). Alternatively, if tables are simple and you want to convert, do so carefully. It might be safer to output tables as HTML `<table>` in the Markdown – Docusaurus will render it fine.
  * Images `<img src="...">` → Markdown image syntax `![alt text](path)` if possible. But if there are custom classes or attributes (width, etc.), you may leave the HTML image tag as is. Docusaurus MDX allows raw HTML, which will pass through.
  * Admonitions: If your Flare content has callouts like Note, Tip, Warning, often these are implemented via snippets (e.g., a “Note” snippet that inserts a styled note box with an icon). After conversion, you’ll have something like a blockquote or a div with a class. You might leverage Docusaurus admonitions syntax for a cleaner result. For example, convert a note like:

    ```html
    <div class="Note"><p><strong>Note:</strong> Remember to save your work.</p></div>
    ```

    into

    ```markdown
    :::note
    Remember to save your work.
    :::
    ```

    This requires recognizing certain patterns (maybe by class name or snippet name). It’s a nice-to-have improvement. At minimum, ensure such content isn’t lost: you can carry over the HTML or convert it to a blockquote (prepend `> ` to each line) to visually distinguish it.
  * Remove any Flare-only artifacts: For instance, Flare might insert an HTML comment like `<!-- MadCap begIndCond: ... -->` around conditional content, or include meta tags for search score, etc. Those should be stripped out. Also remove elements that won’t be used, like `<script src="MadCapAll.js">` or analytics scripts that Flare output might include in each topic – those won’t be needed in Docusaurus.

After this step, each topic should be converted into clean Markdown (with maybe some inline HTML for complex elements).

* **Add YAML frontmatter:** At the top of each Markdown file, include a YAML block with any metadata needed. The most common is `title: "..."` to define the page title (if you want Docusaurus to use it). You might set the title to the same as the Flare topic’s title or the TOC entry title. This ensures the sidebar label or the browser title will show the proper name. If you want custom sidebar labeling or to group in categories manually, you could also assign a `sidebar_label`, but since we are generating sidebars config, we might not need that (the sidebar config can specify the label separately). Other frontmatter could include `slug` if you want to control URL (by default Docusaurus slug is based on file path). For example, if you want `Intro.md` to have URL `/` (home page of docs), you could slug it accordingly or handle that in routing.

* **Filenames and linking:** Ensure that when you write the Markdown files to disk, their file paths correspond to how you referenced them in the sidebar and cross-links. For example, if `TopicA` in Flare linked to `TopicB.htm` via a cross-ref, and you converted `TopicB.htm` to `TopicB.md` in the same folder, then in `TopicA.md` you might have `[...](TopicB.md)`. Docusaurus will transform that into a correct link (during build it might become `TopicB` or `TopicB.html`). Alternatively, Docusaurus supports linking by document ID (which is basically derived from file path relative to docs/). For simplicity, using relative paths in links that mirror your folder layout is effective. Just remember to adjust “.htm” to “.md” in links while converting.

**Important:** Maintain proper linking and avoid broken references. A systematic approach is to keep a map of old Flare file paths to new MD file paths, and use that to rewrite links. Flare’s TOC and cross-ref usage ensures you know which topics connect to which. You may also scan for any plaintext references to “.htm” in content (like if someone hard-coded a hyperlink) and update them.

### 4. Bring Over Assets (Images, Downloads)

Docusaurus by default has a `/static` directory for static assets (which get copied to the build untouched). If you put an image in `static/img/diagram.png`, you can reference it in Markdown as `/img/diagram.png`. Alternatively, Docusaurus allows images to reside alongside the Markdown files (relative links will be transformed). Either approach works; the latter keeps images near content, the former centralizes them.

**Best practice:** Maintain the directory structure for media if possible. For instance, if Flare had `Content/Resources/Images/`, you could create a corresponding `docs/Resources/Images/` and have the MD refer relatively. Or copy all images to `static/img/` and update references accordingly (maybe even flatten if you prefer). The key is to ensure every `<img>` or media file referenced in the MD has a corresponding file in the new project.

Also, transfer any downloadable files (PDFs, etc.) that were linked in Flare, to the static folder and adjust links.

### 5. Verify and Enhance

After conversion, you will have a set of Markdown files and a sidebar definition. At this stage:

* **Build the Docusaurus site** and check that the sidebar appears as expected (same hierarchy as Flare TOC), all pages are present, and navigation (prev/next) goes in the right order (Docusaurus will default to TOC order).

* **Check links:** Click through cross-page links and image links to ensure none are broken. If any links were missed (e.g., a link in Flare that wasn’t in the TOC and you didn’t convert that topic), convert those topics too or adjust the link to an external reference if you chose not to bring that content.

* **Search:** Docusaurus will index the content of your Markdown for search. You might not need to do anything special, but if some important metadata (like Flare index keywords or search synonyms) were present, you could consider adding them as hidden text or using frontmatter tags (Docusaurus can use frontmatter like `tags: ["]` for categories, though not exactly the same as Flare index keywords).

* **Styling adjustments:** If certain styles didn’t carry over (for example, maybe text that was colored or formatted via a class in Flare), you have a couple options:

  * Add custom CSS in Docusaurus (in `src/css/custom.css`) to target those elements or classes. For example, if some paragraphs had a class `.Important` that gave a red highlight in Flare, you can carry that class into the HTML (it would appear in the MD as `<p class="Important">...</p>`) and then define `.markdown .Important { ... }` in Docusaurus CSS.
  * Alternatively, convert those to standard Docusaurus admonitions or other Markdown constructs as mentioned earlier.

* **Table of Contents on pages:** Docusaurus can automatically generate an in-page table of contents for headings (usually displayed on the right side). Flare also had a proxy for mini-TOCs (like a “On this page” for headings) or maybe used *h1 vs h2* to delineate topics vs subtopics. In Markdown, just using appropriate heading levels will let Docusaurus create that mini-TOC. No extra work needed aside from ensuring the hierarchy of headings is logical.

* **Pagination:** If the Flare browse sequence or default previous/next reading order is important, Docusaurus by default will consider the sidebar order as the doc ordering. That should suffice (the sidebar order is our TOC order). If you need a custom ordering separate from sidebar, Docusaurus allows overriding next/prev manually in frontmatter, but likely not needed.

### Summary of Key Recommendations

* **Plan per target** – Extract content using one Flare target’s settings at a time to ensure correct inclusion/exclusion of content and proper variable values.
* **Use XML parsing** – Flare files are XML; leverage that to accurately identify and transform elements (topics, snippets, conditions, xrefs) rather than treating files as plain text. This avoids errors with nested tags or special characters.
* **Merge and replace** – Merge snippets in place and replace variables with their current values so that the Markdown output is self-contained with no dependencies on Flare-specific features.
* **Preserve structure** – Keep the topic hierarchy from the TOC. The user experience in Docusaurus should mirror the Flare help system’s organization. This includes sequence (for next/prev navigation) and grouping (sections).
* **Maintain links** – Ensure all cross-references and hyperlinks become functional links in the static site. Do not hard-code “.htm” extensions; use relative paths or Docusaurus doc IDs that will be resolved. It’s easy to accidentally break links during conversion, so use automated link mapping and consider validating links post-build.
* **Don’t skip the assets** – Copy over all images and media. A missing image in the docs can confuse users; if the Flare output had it, so should the Docusaurus site. Adjust paths in the Markdown or static folder so images load correctly.
* **Test frequently** – As you develop the conversion process, run the Docusaurus site locally to catch formatting issues early. It’s easier to tweak the conversion (e.g., how code snippets or notes are handled) when you can see the outcome immediately.
* **Leverage Docusaurus features** – Take advantage of Markdown enhancements like code blocks (for any sample code from Flare) or admonitions (for notes/warnings) to make the documentation look polished. Docusaurus also supports multi-language content and versioning; if your Flare project had those concepts (maybe via condition tags for version or language), you might integrate with Docusaurus’s approach (e.g., use Docusaurus Versioning for different releases rather than conditions).
* **Document the mapping** – It’s useful to document how each Flare construct was mapped. For example: *Condition “Internal” – excluded from public docs*, *Snippet “NoteBox” – converted to :::note admonition*, *Variable ProductName – replaced with “AcmePro”*, etc. This will help future maintainers understand the decisions made during conversion.


# Converting MadCap Flare Documentation to Docusaurus: Technical Guide

## Docusaurus Structure and Conventions

A Docusaurus documentation site has a particular structure and set of conventions. Understanding these is crucial when mapping Flare content to Docusaurus. The main pieces include the file organization (docs folder, static assets, config files), how sidebars and navigation are defined, how versioning works, and how pages are configured via frontmatter metadata.

### Project File Organization

A typical Docusaurus project (using the classic preset) has the following layout:

```
my-project/
├── docusaurus.config.js        # Site configuration (title, theme, plugins, etc.)
├── sidebars.js (or sidebars.ts)# Sidebar definitions for docs (optional if autogen)
├── docs/                       # Markdown documentation content
│   ├── intro.md
│   ├── guide/                  # Sub-folders group docs by category
│   │   ├── part1.md
│   │   └── part2.md
│   └── tutorials/
│       ├── tutorial1.md
│       └── tutorial2.md
├── static/                     # Static assets (images, PDFs, etc.)
│   └── img/
│       └── logo.png
├── src/
│   └── pages/                  # Custom pages (optional)
│       └── index.js            # Home page if not using docs-only mode
└── package.json (and other build files)
```

In Docusaurus, all files in the `docs/` directory are treated as documentation pages. By default, each Markdown file in `docs` becomes a page under the `/docs/` URL section of the site. This is analogous to Flare topics or HTML files. Organizing docs into subfolders (e.g., `guide/`, `tutorials/`) will by default create corresponding sections in the site’s URL and (if using autogenerated sidebar) in the navigation hierarchy.

**Special Filenames:** If a Markdown file is named `README.md` or `index.md` and is in a folder, Docusaurus treats it as the index of that folder, and by default the URL will use the folder path without the filename. For example, `docs/Guides/README.md` or `docs/Guides/Guides.md` would serve as the “Guides” section landing page at `/docs/Guides` rather than `/docs/Guides/Guides`. This is useful for creating section landing pages (similar to Flare’s concept of book or chapter TOC pages).

**Ignoring Files:** Any file prefixed with an underscore (`_`) in the docs folder is ignored by Docusaurus. This convention is often used for *partials* or include files (like reusable snippets in Markdown, not directly a page). When converting Flare, you might leverage this by outputting snippet content as separate files (prefixed with `_`) if you plan to include them into other docs via MDX import, ensuring they don’t become standalone pages.

**Document IDs and URLs:** Every doc has an *ID* and a *URL*:

* By default, the **document ID** is derived from its path relative to `docs/` (excluding extension). For example, `docs/greeting.md` has ID “greeting”, and `docs/guide/hello.md` has ID “guide/hello”. These IDs are used for linking and for the sidebar configuration.
* The **URL** (slug) by default is also based on the file path. A file `docs/guide/hello.md` becomes accessible at `/docs/guide/hello` (assuming base URL `/docs/`). If a file is named `index.md` in a folder, the URL ends at the folder name (as noted above). You can override URLs with frontmatter if needed (see **Slug** in metadata section below).

**Docs-Only Mode:** Docusaurus can run in “docs-only” mode where the site’s main homepage is one of the docs. If you prefer to have the documentation at the root of the site (instead of under `/docs`), you can adjust the routing in `docusaurus.config.js` (the classic preset allows setting `routeBasePath: '/'` for docs). In a migration context, if you want the new site to mirror the old documentation site’s structure exactly, you might consider docs-only mode so that, for example, `/Introduction` is directly a doc page. Otherwise, keep the default which prefixes all doc URLs with `/docs/` (useful if you also have a landing page or blog).

### Sidebar and Navigation (sidebars.js)

Docusaurus uses *sidebars* to organize docs into a navigation menu (usually displayed on the left for docs pages). The sidebar defines the hierarchy and labeling of docs in the table of contents. There are two main approaches to sidebars:

* **Manually defined sidebars** in the `sidebars.js` (or `.ts`) file.
* **Autogenerated sidebars** based on the file system structure.

**Manual Sidebar Configuration:** In `sidebars.js`, you define an exported JavaScript object (or array) that Docusaurus reads. For example:

```js
// sidebars.js
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Guide',
      items: [
        'intro',             // refers to docs/intro.md by ID
        'guide/part1',       // docs/guide/part1.md
        'guide/part2',       // docs/guide/part2.md
      ],
    },
    {
      type: 'category',
      label: 'Tutorials',
      items: ['tutorials/tutorial1', 'tutorials/tutorial2'],
    },
    { 
      type: 'link', 
      label: 'Project API', 
      href: 'https://example.com/api' 
    }
  ],
};
```

This defines a sidebar with two categories (“Guide” and “Tutorials”) and an external link. Each doc is referenced by its ID (which by default is its file path without extension). A `category` can contain nested items (docs or further sub-categories). A `link` can point to an external URL or another internal route. Manual sidebars give you full control over ordering and grouping. In the above, `'intro'` corresponds to `docs/intro.md`, and `'guide/part1'` corresponds to `docs/guide/part1.md` (because its ID would be “guide/part1”). If you manually define a sidebar like this, any docs not included in it will not appear in the sidebar navigation.

**Autogenerated Sidebar:** Docusaurus can generate a sidebar slice automatically from the folder structure. In `sidebars.js`, this is done by specifying an item of type `'autogenerated'` with a `dirName`. For example:

```js
module.exports = {
  docs: [{ type: 'autogenerated', dirName: '.' }]  // generate sidebar from docs/structure
};
```

This will make Docusaurus traverse the `docs` directory and create categories for subfolders and links for each doc, using file names and frontmatter to determine order and titles. Autogenerated sidebars are convenient for large imports because you don’t have to manually list every file. **Ordering:** By default, autogenerated items are ordered alphabetically by file name. To control order, you can prepend numbers to filenames or use the `sidebar_position` metadata in each doc. For instance, in frontmatter you might put `sidebar_position: 2` to position a doc within its folder category. You can also add a `_category_.json` file in a folder to define the category’s label or order as a whole (including using a float like `2.5` for position).

For the Flare conversion tool, you have a choice:

* **Generate sidebars.js** from Flare’s TOC: This allows preserving the *curated* structure that Flare’s Table of Contents had (which might not strictly match folder structure). The tool can read the Flare TOC XML and produce a corresponding sidebar configuration, mapping each Flare topic to the converted Markdown doc path.
* **Use Autogenerated**: You could also organize the exported Markdown files in directories reflecting the TOC hierarchy and let Docusaurus autogenerate. To ensure correct ordering (since Flare’s TOC order might not be alphabetical), the conversion could add numeric prefixes to filenames or add `sidebar_position` in each file’s frontmatter. For example, prefixing files like `01_Introduction.md, 02_GettingStarted.md` etc., or using frontmatter positions as shown in Docusaurus docs.

**Sidebar Tips:** Keep category and doc labels short for navigation clarity. You can override a doc’s label in the sidebar without changing its title by using the `sidebar_label` frontmatter (or by explicitly naming it in sidebars.js). For complex documentation, nested categories can mirror Flare’s book/chapters. Also, note that sidebars can be split – you can have multiple sidebars (e.g., for different documentation sets) and assign docs to them accordingly, but for most migrations a single unified sidebar is simpler.

### Versioning Structure

If your Flare documentation was versioned (e.g., separate outputs for v1, v2 of a product), Docusaurus’s **versioning** feature can be used. Versioning in Docusaurus allows multiple sets of docs (e.g., “latest” and older versions) to coexist. Key points:

* You generate a version by running `docusaurus docs:version <versionName>`. This copies the current `docs/` content into a new directory under `versioned_docs/` and freezes it.
* The project will create a `versions.json` file and a `versioned_sidebars/` file for that version’s sidebar. For example, after versioning, you might have:

  * `docs/` (continues to be the working set for “next” or unreleased docs).
  * `versioned_docs/version-1.0/` (snapshot of docs at v1.0).
  * `versioned_docs/version-2.0/` (snapshot for v2.0, etc.).
  * `versioned_sidebars/version-1.0-sidebars.json` for the sidebar of that version.
* Docusaurus URLs for versions: By default, the “latest” version (e.g., 1.0 if that’s the newest) will still use `/docs/` base, and older versions get prefixed (e.g., `/docs/1.0/...`). You can configure which version is treated as the main/default.

If you plan to migrate multiple Flare outputs (like separate projects or versions), you could import one as the initial docs, then run the versioning command, then import the next, etc., or manually place content into the versioned_docs structure. **Alternatively**, if Flare used conditional text for versions rather than separate projects, you might split those by running the conversion for each version of the content and leveraging Docusaurus versions to host them side by side.

**Versioning Considerations:** It’s often easiest to perform the conversion for the latest documentation first (into `docs/`), get everything working, then use Docusaurus to create a version snapshot and then replace the `docs/` with the next version’s content. The sidebar can often be similar between versions, but if not, you can generate separate sidebars for each. Docusaurus’s versioning yields a structure like `docs/` (current) + `versioned_docs/` (past versions), with Docusaurus knowing to route appropriately. If you don’t need versioned docs, simply ignore this feature and keep one set of Markdown files.

### Metadata Frontmatter in Markdown Files

Every Markdown/MDX file in Docusaurus can have a **YAML frontmatter** block at the top (between `---` lines). This frontmatter provides metadata that Docusaurus uses for routing, labeling, and behavior of the doc. While frontmatter is optional (Docusaurus can infer some things), it is highly recommended to include certain fields for a migrated doc set. Important frontmatter fields include:

* **id:** Manually sets the document’s unique ID (overriding the default path-derived ID). Use this if you want an ID different from the filename or need to ensure consistency regardless of file location. For example, `id: getting-started` in `intro.md` will make its ID “getting-started” instead of “intro”. *If you use a custom `id`, note that it also influences the default URL (slug) in Docusaurus v2+*.
* **title:** The title of the document. This is used as the H1 heading shown on the page (unless you hide the title) and in the page’s `<title>` for SEO. If no frontmatter title is given, Docusaurus will use the first markdown heading in the content as the title. We suggest setting `title` explicitly for clarity (especially if you plan to hide the autogenerated heading).
* **slug:** Allows you to set a custom URL path for the document. By default, a doc’s URL is derived from its file path. If you want to, say, flatten the URL or change it, you can use `slug`. Example: in `guide/intro.md`, `slug: /introduction` would make the page accessible at `/docs/introduction` instead of `/docs/guide/intro`. Use this sparingly for special cases (like making a doc the home of docs section).
* **sidebar_label:** If you are using an autogenerated sidebar, this label will be used for the doc in the sidebar instead of the title. This is useful if your page title is long but you want a shorter label in the nav. For manually written sidebars, you can also just put the desired label in the sidebars.js file itself.
* **sidebar_position:** A numeric position for ordering in an autogenerated sidebar. Docs within the same folder (or category) will be sorted by this (ascending). It can be an integer or float (you might use 1.1, 1.2 for fine control). If not provided, alphabetical by file name is default. In Flare, topics are ordered in the TOC – capturing that order can be done by assigning sidebar_position values in the conversion process.
* **description:** A short description of the page, used in the `<meta>` description for SEO and sometimes in search results preview. This is not visible on the page but good to include (one or two sentences summarizing the topic).
* **tags:** You can assign tags (an array of strings) to docs. This is optional, but Docusaurus can generate tag listing pages if you use this. If Flare had index keywords or categories, you might map those to tags in Markdown.
* **hide_title:** Set to `true` to not display the title on the page. By default, Docusaurus will render the `title` (or the first heading) as an H1 at the top of the content. If your Markdown already includes an H1 that you want to keep (for styling or legacy reasons), you might end up with duplicate titles. Setting `hide_title: true` will prevent the default title from showing, so you can use your own in the content.
* **hide_table_of_contents:** Set to `true` to disable the right-hand table of contents for that page. By default, Docusaurus generates a mini-TOC on the right side listing the headings in the page. If a page is very short or you don’t want that, you can hide it.

An example frontmatter for a doc might look like:

```yaml
---
id: install-guide
title: "Installation Guide"
slug: /install
sidebar_label: "Install"
sidebar_position: 3
description: "How to install and configure the application."
tags: [Setup, Release1.0]
---
```

In the above example, the file might be `docs/setup/install.md` originally, but we set a custom `id` and `slug` so it will appear at URL `/docs/install` and have a specific sidebar label and order. Docusaurus will use these values when generating the site navigation. (If this doc is part of an autogenerated sidebar, it will show with label “Install” in position 3 in its category; if manual, we’d refer to it by `id: install-guide` in sidebars.js.)

**Note:** Frontmatter must be at the very top of the file and bounded by `---` lines. Ensure the YAML is valid (e.g., strings in quotes if they contain special characters). The conversion tool should populate at least `title` (from the Flare topic title) and possibly `id` (maybe using Flare’s topic ID or file name) and any other needed fields like `sidebar_position`. If the conversion output will use an autogenerated sidebar, including `sidebar_position` for each doc according to the Flare TOC order is very helpful; if a manual sidebar is output, then the order is controlled in sidebars.js.

### Custom Components and MDX Integration

One powerful aspect of Docusaurus is that all docs are MDX (Markdown with JSX). This means you can extend content with React components or dynamic content. When converting from Flare:

* **Reusing Content (Snippets):** Flare snippets are reusable chunks. Docusaurus doesn’t have an out-of-the-box snippet mechanism, but you can simulate it with MDX. For example, you could convert a Flare snippet to a Markdown file (perhaps in a `_includes` or `_shared` folder, prefixed with `_` so it’s ignored as a standalone page). Then in any MDX doc, you can import it and use it as a component. E.g., in `myDoc.mdx`:

  ```jsx
  import SnippetContent from '@site/docs/_shared/mySnippet.md';
  …  
  <SnippetContent />
  ```

  This will include the content of `mySnippet.md` at that point. (Alternatively, convert snippets directly into static content in each topic during conversion to keep things simpler.)
* **Special Formatting:** If Flare topics used styled text boxes for notes, tips, warnings, etc., you can map these to Docusaurus admonitions. For instance, a Flare “Note” text box can become `:::note ... :::` in Markdown. The conversion tool might detect certain icons or styles in the HTML and inject the admonition syntax or a custom admonition if needed. Docusaurus’s default admonitions cover many common callouts (Note, Tip, Info, Caution, Danger).
* **Conditional Content:** Flare conditions allow including/excluding content per target. Docusaurus has no direct equivalent of conditional text in Markdown. If some content was conditional in Flare and you need to carry that logic over, you have a few options:

  * Generate separate versions or separate docs for each condition state (for example, if a section was Windows vs Linux content, you could split into two docs or use tabs).
  * Use MDX to create a custom React component that conditionally renders content based on some site context (this requires writing a plugin or some global state, which is advanced). In most cases, it’s simpler to resolve conditions at conversion time, producing static content for one chosen output or duplicating sections if needed.
* **Interactive or Dynamic Content:** With MDX, you can embed things like API interactive consoles, diagrams (there’s a plugin for Mermaid diagrams, for example), or other React components. Identify if any Flare content (e.g. HTML5 widgets or scripts) need replacement. Docusaurus can embed raw HTML/JS, but often a React reimplementation is cleaner. Plugins exist for things like Mermaid charts, math equations, etc., which might be relevant if Flare used any script for those.
* **Global Variables:** Flare’s variables (e.g., product name variables) would typically be resolved to text during conversion for a static site. Alternatively, Docusaurus could use React context or environment variables, but that complicates the setup. The straightforward approach is to replace Flare variables with their value when generating Markdown. However, if the tool needed to handle multiple product variants, you could output a separate Markdown version for each variant or instruct authors to use a simple placeholder and then do a find-replace in the content build. Generally, since Docusaurus treats content as code, having dynamic variables inside is not typical (aside from versioning and translation which are separate concerns).

In summary, Docusaurus’s MDX allows a lot of flexibility. For an automated conversion, it might be wise to keep the output Markdown as simple as possible (favoring static content) and only use MDX enhancements for things you *cannot represent in plain Markdown*. This reduces the chance of introducing errors and makes the converted content easier to maintain by documentation writers in the future (they can edit Markdown without needing to know React, in most cases).

## 3. Required and Recommended Metadata in Docusaurus Markdown

**Frontmatter Best Practices:** As noted, Docusaurus does not strictly *require* frontmatter in each doc (it will infer title from first heading, id from filename, etc. by default). However, including frontmatter is recommended to ensure consistency. Here are the key metadata fields to include in each Markdown file after conversion:

* **title:** Provide a title for each page. In Flare, the topic title can be used here. This ensures the page has an H1 and is labeled correctly.
* **id (optional):** If you want to control the document ID (especially for linking or if file names are not ideal identifiers), set an `id`. One scenario: if Flare file names are cryptic (e.g., `TOPIC_ABC123.htm`), you might name the Markdown file more nicely (e.g., `getting-started.md`) and set `id: topic-getting-started` or similar. However, you can often skip setting `id` and let Docusaurus derive it from the file name, which will be the simpler approach if the filenames are already meaningful.
* **slug (optional):** Use only if you need to override the URL path. For example, to match an old URL structure or to shorten a deeply nested path. If not set, the default `/docs/` + path is used. Only a subset of pages may need this (like if you want one doc to be the root `/docs/` or you want to flatten one level).
* **sidebar_label:** For autogenerated sidebars, if a page’s title is too long to show in navigation, you can set a shorter `sidebar_label`. For example, a page titled “How to Install the XYZ Product on Windows and Linux” might have a sidebar_label: “Installation”. In manual sidebars, you control labels directly in the config, so this is mainly for autogen convenience.
* **sidebar_position:** If using autogen sidebars, include this for every doc to reflect the TOC order from Flare. If generating a manual sidebar, you can skip this (since order is in sidebars.js). But it doesn’t hurt to include; it just won’t be used in manual scenario.
* **description:** Adding a one-line description frontmatter helps SEO and provides a hover preview if using search plugins. Flare’s topics might have an abstract or short description which you can use here.
* **others:** `tags` if categorizing content, or any Docusaurus-specific flags like `draft: true` (if you want to exclude a page from production builds, e.g., if some topics are not ready – note that `draft` is a relatively new frontmatter option in Docusaurus).

When generating frontmatter via a script, ensure YAML syntax is correct. Also remember that in Docusaurus v2+, specifying an `id` effectively sets the slug to `/{id}` if slug is not separately provided. So if you set `id`, the page URL may change from the file-based path. If preserving path is important, you might actually avoid setting `id` unless necessary (or set both `id` and `slug` to maintain a certain structure).

**Minimal frontmatter vs. explicit:** For a straightforward migration, you might include just:

```yaml
---
title: "Original Topic Title"
---
```

and let everything else be default. Docusaurus will generate an ID from the file name and a URL accordingly, and use the title for display. However, to precisely control ordering and ensure future stability, adding `sidebar_position` and a custom `id` can be good. It’s a balance between effort and need:

* If you want **human-friendly file names** to double as IDs/URLs, you can rely on those and keep frontmatter minimal.
* If you want to decouple **IDs from file names** (maybe to allow renaming files later without breaking links), use the `id` field consistently and use those IDs in any cross-links and sidebars.

**Frontmatter and Warnings:** Docusaurus will warn or error if there are duplicate IDs. So ensure all `id` values are unique across all docs (including across versioned docs). Also, if you accidentally reference an ID in sidebars or links that doesn’t exist, you will get a broken link error on build (more on link checking in a later section). Use a systematic naming scheme for ids if you set them (e.g., prefix with section or use full path as id) to avoid collisions.

In summary, the *required* metadata is essentially just a title (to avoid having to put an H1 in the Markdown manually), but the *recommended* metadata includes sidebar ordering and any custom slugs/IDs needed to preserve structure. By planning the frontmatter fields, your converted docs will integrate smoothly into Docusaurus and behave as expected in navigation.

## 4. Handling Static Assets (Images, PDFs) in Docusaurus

Documentation often includes images, diagrams, PDFs, and other assets. Docusaurus can handle these, but the approach differs from Flare’s storage of resources. Here’s how Docusaurus manages static assets and how to properly link them:

**Static Folder vs. Asset Co-location:** By default, Docusaurus provides a `static/` directory for assets. Any file placed in `static` will be copied directly into the final build output (preserving relative paths). For example, `static/img/picture.png` ends up as `site.com/img/picture.png` in the deployed site. The benefit of `static` is that you can reference files by a simple path and they don’t go through Webpack processing. However, Docusaurus also supports **co-locating assets** in the docs folders and will bundle them:

* If you write a Markdown link or image with an absolute path (starting with `/`), Docusaurus looks in the static folder for that file. E.g. `![Diagram](/img/diagram.svg)` will be resolved to `static/img/diagram.svg` (or `public/img/diagram.svg`) if it exists. During site build, it actually converts that to a webpack require and appends a hash to the filename for cache-busting.
* If you use a relative path in Markdown (e.g. `![Diagram](./images/diagram.svg)` where `images/diagram.svg` is a file alongside the MD file), Docusaurus will treat it similarly by bundling it. In fact, Docusaurus **automatically converts markdown references to images or files into require() calls** so that you can colocate assets with docs. This means you are not forced to dump all images into `static/` if you prefer to keep them next to the content.

**Best Practice:** You have two options for organizing images:

1. **All in static/** – e.g., put all Flare images into `static/img/flare/…` and update image references in Markdown to absolute paths like `/img/flare/imagename.png`. This approach makes it clear where assets live and is straightforward (similar to Flare’s centralized *Content Explorer*). The images in static can be referenced directly and will not be hashed or processed (they are served as-is).
2. **Co-locate with docs** – e.g., for each doc or section, put its images in a subfolder alongside the Markdown. Update image references to relative paths. For example, in `docs/guide/part1.md`, reference an image `![UI](./part1_assets/screen.png)`. Docusaurus will bundle that image, copying it to the build assets and giving it a hashed filename for caching. This keeps images near the content, which can be easier to manage for authors and prevents the `static` folder from becoming a huge dumping ground.

Both approaches are valid. Co-location often results in a tidier project structure for large doc sets (you could mimic Flare’s *Topics and images in same folder* organization, if that was how the Flare project was laid out). The conversion tool can either copy all media from Flare into `static/` or mirror the Flare project folder hierarchy under `docs/` (with images in subfolders). Note that if you co-locate, your Markdown links should be **relative** (Docusaurus will convert them to webpack require calls automatically, ensuring the links work and broken references are caught at build time).

**Linking to Files (PDF, etc.):** The same rules apply. If you have a PDF user guide to link, you can put it in `static/files/Guide.pdf` and then in Markdown do: `[Download Guide](/files/Guide.pdf)`. This will be transformed into a runtime link that goes to the correct location (with base URL accounted for). Behind the scenes, it becomes something like `<a href={require('static/files/Guide.pdf')}>Download Guide</a>` in the React code. If a file is co-located (say `docs/manuals/install.pdf` and you do `[Install PDF](./manuals/install.pdf)` in Markdown), that also gets included via Webpack require (so the PDF will end up hashed in the build output, e.g., `install.abc123.pdf` in `assets/files` and the link will point to that). A benefit of this bundling is that missing files are caught early (if the file isn’t found, the build will error).

**Image Handling Differences:** If images are in `static/`, you refer to them with absolute path and they are not processed (no resizing or optimizing by default, just copied). If you use the MDX built-in image handling (importing or requiring images), you could potentially leverage image optimization plugins (like `@docusaurus/plugin-ideal-image` for responsive images). However, initially, simply migrating images over without altering them is fine. Keep in mind:

* Docusaurus will not compress or optimize images by itself (except for the optional IdealImage plugin). So large PNGs from Flare remain large PNGs. Consider optimizing images if size is an issue.
* The `static/` approach will keep file names identical (useful if you want to preserve exact names for some reason). The co-located approach will give hashed names in the final output (which is fine for browsers and improves caching, but if someone knew the direct image URL, it won’t be human-readable).

**Linking Examples:**
In Markdown (Docusaurus):

```markdown
Check this figure:

![Architecture Diagram](/img/architecture.png)

For details, see [Appendix PDF](/files/Appendix.pdf).
```

During build, Docusaurus will check `/static/img/architecture.png` and `/static/files/Appendix.pdf` exist (or in `public/` if configured). It will transform the Markdown into HTML like:

```html
<img src={require('static/img/architecture.png').default} alt="Architecture Diagram" />
<a href={require('static/files/Appendix.pdf')}>Appendix PDF</a>
```

This ensures the base URL is handled and that a missing file would trigger an error. If using relative paths, the require call will use a relative module path instead. The main point is: **use Markdown syntax for links and images**, not raw `<img>` or `<a>` tags, so that Docusaurus can process them. If you use a raw HTML `<img src="...">`, Docusaurus will leave it as-is (and it won’t adjust base URL or catch missing file issues).

**Edge Cases:** If your docs are going to be translated using Docusaurus i18n, assets co-located in docs have to be duplicated for each language (because each locale has its own docs folder). In that case, using the static folder for images might be easier to avoid duplication. If not translating, this is not a concern.

**Conclusion on Assets:** The conversion script should extract all images from Flare (often Flare outputs them to a resources folder or leaves them as linked files). You’ll then import those into the Docusaurus project. If Flare had an `Images` subfolder with the same hierarchy as topics, you can mirror that. Update the Markdown image references accordingly. As a quick strategy, consider copying all images to `static/img/` and doing a find-replace on the HTML `<img src="...">` to Markdown `![](path)` with the appropriate path. Or for more structure, place images next to their docs and adjust paths. In either case, Docusaurus will be able to serve them. Remember to test that all images appear and files download correctly by running the Docusaurus dev server after conversion.

## 5. Docusaurus Plugin Ecosystem for Automation and Extension

Docusaurus is highly extensible via plugins. In fact, nearly every feature (docs, blog, pages, search) is implemented as a plugin. For someone migrating content, certain plugins can be very helpful, and understanding the ecosystem allows you to plan for future enhancements or automation beyond the initial conversion.

**Core Plugins:** The *docs plugin* (`@docusaurus/plugin-content-docs`) is what provides the documentation functionality. It’s included by default in the classic preset. Similarly, there is a blog plugin for blog support and a pages plugin for static pages. Typically, you won’t need to touch these directly, but it’s good to know they exist. The docs plugin has configuration options for path, route base, sidebar items, versioning, etc. (mostly set via `preset-classic` config in `docusaurus.config.js`).

**Official Plugins:** Docusaurus offers official plugins for things like search (Algolia DocSearch), Google Analytics, sitemap generation, client-side redirects, PWA support, etc. For a documentation migration, two notable ones are:

* **Client-Side Redirects Plugin:** `@docusaurus/plugin-client-redirects` can generate HTML stub pages to redirect from old URLs to new ones. If your Flare site URLs were different and you want to preserve those incoming links, you can configure this plugin with rules. For example, if Flare had a page at `/Content/Install.htm` and now your Docusaurus page is `/docs/install`, you can set up a redirect from `/Content/Install.htm` to `/docs/install`. The plugin will create an HTML file at the old path that immediately redirects to the new one. This is very useful for not breaking external hyperlinks or bookmarks after migration.
* **Search plugin (Algolia):** If you host publicly and want full-text search, the Algolia DocSearch is integrated via `@docusaurus/theme-search-algolia`. Not directly related to conversion, but good to plan so that once docs are up, they are searchable. If not using Algolia, there’s a community plugin for local search as well.

**Community and Custom Plugins:** The community has many plugins. For example, since you are converting from an external source, one interesting plugin is **docusaurus-plugin-remote-content**. This plugin allows pulling in Markdown content from external repositories or URLs at build time. In theory, one could use it to fetch content from a source and include it. However, in the case of Flare, it’s not directly applicable unless you, say, exported Flare content to a publicly accessible place. More relevant might be writing a custom script to generate files (rather than doing it in a plugin).

**Using a Plugin vs. Preprocessing:** You might wonder if the conversion process itself could be a Docusaurus plugin – for instance, a plugin that reads Flare XML and generates pages. While possible (Docusaurus plugins can generate content before compilation), it is typically easier to perform conversion as a separate build step (using Python or a script) and treat the result as static Markdown input to Docusaurus. The plugin system is more useful once the content is Markdown:

* You could create a Remark or Rehype plugin to handle any special syntax in the Markdown. For example, if some Flare-specific placeholders made it through conversion, a custom Remark plugin could replace or transform them during the Docusaurus build. The Docusaurus config allows adding Remark/rehype plugins in the content pipeline.
* If you needed to integrate dynamic content (like pulling in API documentation from code), there are plugins for OpenAPI docs, GraphQL docs, etc., which might be of interest if your documentation includes those.

**Extending the Docs with MDX Components:** Not exactly a plugin, but Docusaurus allows *theme components* to be swizzled (overridden) and custom React components to be used. For example, if after conversion you find you want a custom UI element to mimic some Flare feature (say an expanding drop-down text), you could implement that as a React component and embed it via MDX. This doesn’t require a plugin, just placing the component in `src/components` and importing it where needed.

**Maintaining and Automating:** Once your docs are on Docusaurus, you can leverage typical web toolchains:

* Use **CI/CD** pipelines (like GitHub Actions) to auto-deploy the site on content changes.
* Use linting tools (we’ll cover in next section) that can be integrated as plugin or as separate scripts.
* If your conversion tool remains in Python, you could integrate it into the build process (e.g., have a script that regenerates the Markdown from Flare source or Flare output whenever needed, then runs Docusaurus build).

**Internationalization Plugin:** If you plan to translate docs (Flare has multilingual output features, and Docusaurus supports i18n), the i18n system is built-in (not an external plugin, but part of core). It generates copies of docs for each locale. This might be an area of extension if you migrate Flare’s multi-language projects – Docusaurus expects you to provide translated Markdown in separate folders or use Crowdin integration.

In summary, Docusaurus’s plugin ecosystem can **aid automation** by providing features that you might otherwise custom-build. Particularly, the redirect plugin helps preserve old links (so you don’t lose SEO or user bookmarks), and community plugins like remote-content or others could be handy for edge cases. The docs plugin itself will do a lot (generate sidebars if needed, handle versioning). Always check the \[Docusaurus Community Plugin Directory] if you have a certain need – for example, there might be a plugin to generate a glossary or index from Markdown, or to embed interactive diagrams, which could replace similar features from Flare.

## 6. Validation and Automation Tools for Converted Markdown

Quality assurance is essential after converting a large documentation set. You want to ensure the Markdown is well-formed, links are correct, and the content adheres to expected standards. Several tools and approaches can help:

**Docusaurus Build Warnings/Errors:** Docusaurus itself will catch certain issues:

* **Broken Links:** If any page contains a link to another doc that Docusaurus cannot resolve (e.g., bad URL or wrong doc ID), the build will error out with a message listing broken links. For example, if `[see here](nonexistent.md)` is in your Markdown but there’s no doc with that id or path, you’ll get a “Docusaurus found broken links” error at build time. This is extremely useful for validation. As a practice, keep the `onBrokenLinks` setting to `throw` (the default) during development, so you catch and fix all broken links. (You can set it to `warn` in production if you need to deploy with known issues, but ideally, resolve them.)
* **Broken Images:** Similar to links, if an image or file is referenced and the file is missing, the webpack require will fail. You’ll see errors during the build (or the dev server console) about missing modules. This ensures you don’t ship pages with missing images—fix any file paths that are wrong.
* **Duplicate IDs:** Docusaurus will warn if two docs end up with the same id (which can happen if you manually set id or if two files have the same name in different folders without a folder prefix). Make sure each doc id is unique; the conversion script can enforce this by, for example, prefixing IDs with a category or using full paths.

By running `npm run build` (or `yarn build`) on the site after conversion, you’ll surface these errors. Even the development server (`npm run start`) might log warnings for some issues, but the production build is stricter.

**Markdown Linting:** Use a linter to catch Markdown style issues:

* **markdownlint** (NodeJS) or its CLI can enforce rules like “no trailing spaces”, “ordered list numbers should increment”, “proper heading levels”, etc. You can adopt a Markdown style guide to keep consistency.
* **remark-lint** (part of the remark toolchain, which Docusaurus already uses under the hood) can be configured with plugins to check for specific patterns. For instance, ensuring that headings are title-cased or checking that all links have text.
* These can be run as part of CI to ensure any manual edits to Markdown don’t introduce formatting issues.

**Link Checkers:** Although Docusaurus catches internal broken links, you might also have external links in your docs. It’s good to run a link checker on the built site or directly on Markdown:

* Tools like **Broken Link Checker** or **blc** (for websites) or **lychee** (a link checker that can parse Markdown) can verify that external URLs return OK. This is more for ongoing maintenance, but worth doing after the conversion because some links might have been carried over from Flare and could be outdated.
* Docusaurus doesn’t automatically check external links; a separate run of a tool or a script is needed for that.

**Spell Checking / Grammar:** When converting, especially if using an automated tool, some odd text artifacts might slip in (for example, if HTML entities weren’t properly handled or if conditional text left some seams). Running a spell checker over the Markdown can catch obvious typos. Tools:

* **Spellcheck GitHub Action**: There are GH Actions that scan for spelling mistakes in the repo.
* **Vale**: A popular “lint” for prose style and terminology. You can set up Vale with a vocabulary (e.g., ensuring product names are spelled correctly, avoiding certain phrases) to maintain consistency similar to how Flare’s condition tags might enforce terminology differences.

**MDX Validation:** MDX is Markdown plus JSX, which is more complex to parse. If your Markdown linter doesn’t understand MDX, it might flag valid MDX syntax as errors. You might integrate **Prettier** (with an MDX plugin) to auto-format and thereby indirectly validate the MDX syntax. Prettier can reformat your docs uniformly (e.g., consistent list indentation, code fence styling), which can catch issues (since if Prettier fails, there might be a syntax problem).

**Unit Testing Content:** In some migrations, teams even write small scripts to verify content conversion. For instance:

* Check that every Flare topic resulted in a Markdown file.
* Check that certain known phrases exist (content not lost).
* If there were Flare micro content or snippets, verify they appear in all the right places in the MD (maybe via searching for unique text).

**Continuous Integration:** Automate these checks:

* Set up a CI pipeline that runs the Docusaurus build (to catch build errors) and runs linters/tests on every pull request or commit. This way, if someone inadvertently breaks a link or format in the Markdown in the future, it’s caught immediately.
* You can also add a step to your CI to run the conversion tool itself (if you treat Flare as the source of truth and want to regenerate Markdown as part of the process). However, in practice once you migrate off Flare, you might stop using Flare and maintain only the Markdown going forward (docs-as-code approach).

**Testing the Site:** After building, do a manual or automated run through the static site:

* Use a headless browser or a tool like Cypress/Selenium to click through links from the homepage to ensure navigation works (this can be scripted by crawling the built site).
* Ensure the search (if configured) indexes the content (usually tested by running the site and using the search bar).

By combining Docusaurus’s own checks (which are quite helpful) with external linting and testing, you can establish a robust quality gate. As a developer of the conversion tool, you might also include a “verify” mode in your tool that logs, for example, how many topics, images, snippets were processed, and if any known construct was not handled (maybe count of "WARNING: unresolved xref" if your tool couldn’t find a target).

**Example – Catching a Broken Link:** Suppose in Flare a topic had a cross-reference to another topic that got renamed or dropped, and your conversion yields `[See XYZ](missing-topic.md)`. When running `npm run build`, Docusaurus will output an error like: *"Error: Docusaurus found broken links! Please check the pages of your site in the list below, and make sure you don't reference any path that does not exist..."*. It will list which page and which link is problematic. This direct feedback pinpoints issues to fix before publishing. You can also configure in docusaurus.config `onBrokenLinks: 'throw'` (default) or `'warn'` if you temporarily want to ignore them, but throwing is recommended to not miss anything.

**Final sanity checks:** Validate that the site’s content looks correct:

* Paragraphs aren’t inadvertently combined or broken (could happen if a missing blank line in Markdown – a lint rule can catch that).
* Code blocks render properly (no stray HTML).
* Tables look okay (complex tables from Flare might need adjustment if they were using colspan/rowspan heavily, since GFM tables have limitations).

In essence, treat the docs like code: use linters, automated tests, and CI to ensure the converted Markdown is robust and remains that way with future edits. This “docs as code” philosophy is one reason to migrate to a system like Docusaurus in the first place, and it will pay off in documentation quality.

## 7. Tooling for Converting Flare (XML/HTML) to Markdown

Developing an open-source conversion tool from MadCap Flare to Markdown involves parsing Flare’s output (or source) and converting the structure (TOC, topics, links, media) to a format suitable for Docusaurus. Here we discuss useful libraries and approaches, primarily focusing on Python (as requested) but also noting other options.

### Source of Flare Content

First, decide **what input** your tool will use:

* *Flare-generated HTML/XHTML output*: Flare can produce HTML5 or XHTML files for each topic when you build a target (like an HTML5 Help output). These files have the content after applying conditions and variables, which is very handy – it means you get the final expanded text. Using this as input is straightforward: each HTML file corresponds to a topic. The downsides: you lose some info like topic IDs (though they might be in attributes), and cross-reference links might be in the form of HTML file links (which you’ll need to map).
* *Flare source XML*: Flare’s source topics (.flhtm or .xml) contain proprietary tags (MadCap-specific XML). Directly parsing those would let you potentially extract more semantic info (like snippet references, conditions, etc.), but you would then have to implement logic for applying conditions and variables much like Flare does – a complex task. It might be easier to let Flare do that by generating an output.
* *Flare TOC file*: Flare’s TOC is stored in an .fltoc XML file (or multiple). This gives the hierarchy of topics and their titles as used in the TOC. If available, parsing this will help create the Docusaurus sidebar in the correct order.

A recommended approach is: **Export a Flare target to XHTML** (Flare has a “XHTML” target or you can configure the HTML5 target to produce clean XHTML) and use that as your raw data. Ensure that in the target you select all necessary condition tags and set variables appropriately so the output is exactly what you want in the docs.

### Parsing and Converting HTML to Markdown

Once you have HTML for each topic, the main task is converting HTML markup to Markdown. There are libraries to help:

**Python Libraries:**

* **Beautiful Soup (bs4):** Great for parsing HTML into a tree. You can traverse and manually convert nodes to Markdown text. For example, find all `<h1>` to `<h6>` tags and replace them with `#`...`######` text, convert `<p>` to just text (with two newlines after for paragraph separation), `<strong>` to `**` etc. This gives you fine control, but writing a full HTML-to-Markdown converter from scratch is time-consuming.
* **markdownify / html2markdown:** These libraries do automatic HTML to Markdown conversion. `markdownify` (and its fork `html-to-markdown`) can take an HTML string and return a Markdown string, handling common tags. You can often customize rules. For instance, `html_to_markdown` allows providing custom handling for certain tags (like maybe you want `<img>` to be converted in a particular way). Using such a library can jump-start the conversion. For example:

  ```python
  from html_to_markdown import convert_to_markdown  
  md = convert_to_markdown(html_string)
  ```

  would yield a Markdown text with basic formatting done.
* **Pandoc via pypandoc:** Pandoc is a powerful document converter supporting many formats. Using `pypandoc`, you could convert HTML to GFM Markdown. Pandoc tends to produce very clean Markdown, but you might need to tweak options (e.g., how it handles headings or lists). One advantage: Pandoc could potentially parse Flare’s XML if given a suitable reader, but that’s advanced. Simpler is HTML->Markdown with Pandoc. The downside might be adding a dependency on the Pandoc binary (Haskell-based).
* **Others:** `html2text` (another library) or `Bleach` for sanitizing, etc., but markdownify and html-to-markdown are more focused for this use case.

**Algorithm with Libraries + Custom Rules:**
No converter library will perfectly handle all aspects out-of-the-box, because Flare’s HTML might have some unique patterns:

* *Headings:* Ensure the top-level heading in each topic becomes a first-level Markdown heading (`# Title`). Flare topics often have `<h1>` as the title in the output. The converter should take that text for the Markdown file’s title (frontmatter or first heading). You might even strip the `<h1>` from the content and use it in frontmatter `title`.
* *Lists:* Flare’s HTML for lists is standard `<ul><li>` or `<ol><li>`. Libraries will convert those to `-` or `1.` lists fine. Watch out for nested lists – proper indentation in Markdown is needed.
* *Images:* Flare might output `<img src="Images/img.png" alt="...">`. The converter library might produce `![alt text](Images/img.png)`. You will likely need to adjust the path (e.g., `Images/img.png` might need to become `../static/img/...` or wherever you decide). Possibly post-process image links in the Markdown to point to the right location in Docusaurus.
* *Links (cross-references):* In Flare HTML, links to other topics might be something like `<a href="../Output/Topic.htm">See Topic</a>` or with an anchor. You need to rewrite these to Markdown links pointing to the corresponding MD files. If your conversion maintains a mapping of old filenames to new filenames/IDs, you can replace the href accordingly. For example, if `Topic.htm` became `topic.md` (with id “topic”), you’d output `[See Topic](./topic.md)` or just `(topic)` (if using Docusaurus link by id shorthand, which is not directly supported unless you use `<Link>` component). The simplest is using relative paths that mirror the folder structure of docs.
* *Tables:* HTML tables can be converted to GFM tables by markdownify, but complex tables (with merged cells) might not translate well because GFM doesn’t support row/col span. You might need to detect such cases and perhaps leave them as HTML (which Docusaurus can handle if you allow raw HTML). You could wrap them in an `<div dangerouslySetInnerHTML>` in MDX if needed, but better is to simplify tables if possible.
* *Code snippets:* Flare might output `<pre><code class="language-js">...</code></pre>` for code blocks. The converter should turn those into \`\`\`js fenced blocks. If using a library, verify that it picks up the class as the language identifier. If not, a custom rule may be needed to post-process code blocks.
* *Snippets and conditions:* If you use Flare’s output after conditions and snippet resolution, ideally those are already resolved and you have a static result. But double-check: sometimes Flare leaves markers in the output (like an HTML comment `<!-- snippet: ... -->`). If so, you might remove those via a regex or parser before converting to Markdown. Same with conditions: excluded content won’t be there, included content is just normal HTML.
* *Flare-specific tags:* Flare sometimes adds wrapper `<div>`s or spans with classes (for drop-down text, etc.). For example, expanding text in Flare might be a `<div class="DropDownTitle">...` followed by a hidden `<div class="DropDownBody">...</div>`. Markdown has no direct equivalent, but you could convert that pattern into a Docusaurus `<details><summary>` HTML block or an admonition. The tool may need special-case handling for such interactive content. If such features are heavily used, identify them and decide how to handle (maybe output a note that “feature not converted” or implement a custom markdown syntax for it).
* *Variables:* If the Flare output still contains placeholders (ideally it shouldn’t if output is final), replace them. If the conversion is reading Flare source, you’d need to substitute variables using some input of variable definitions.

**Generating Sidebars:** After converting all topics to Markdown files (saved in some `docs` subfolders), you need to create `sidebars.js` or rely on autogen. If you choose autogen, you might still want to create `_category_.json` files for each folder to set the category label (because the folder name might not be the desired label). For example, if Flare TOC had a node "User Guide" containing topics, you might have put those topics in `docs/UserGuide/*`. By adding a `docs/UserGuide/_category_.json` with `{ "label": "User Guide" }`, the sidebar category will show as "User Guide" instead of "UserGuide" (folder name). You can also set `position` in that JSON to place that category among others.

If you prefer a **single sidebars.js** definition (manual):

* Parse the Flare TOC XML. Each TOC entry has a title and a link to a topic file. You can produce a nested data structure (e.g., a Python list/dict) reflecting that. Then output it as a JS module syntax. Since sidebars.js is just data, you could even output JSON and `module.exports = require('./sidebar.json')` in the JS, but typically one writes directly in JS format.
* Example: if TOC has Book "Guide" with child topics "Intro", "Install", and Book "Reference" with topics "FAQ", you'd produce something akin to the earlier sidebars example with nested categories.
* Ensure that the IDs or paths you reference match the converted docs. If you set custom ids in frontmatter, use those; otherwise use relative paths (which Docusaurus resolves to ids). For instance, if `install.md` has no id frontmatter, its id is "install", so in sidebars you reference `'install'`. If it’s in a subfolder, id is `subfolder/filename`. Keep these consistent.
