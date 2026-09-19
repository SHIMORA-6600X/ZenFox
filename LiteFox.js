/****************************************************************************
 * LiteFox                                                                 *
 * "SHIMORA"                                                *
 * priority: Debloat Firefox                                             *
 * version: 156                                                             *
 * url: https://github.com/SHIMORA-6600X/ZenFox                           *
 * license: MIT
 ***************************************************************************/

/****************************************************************************
 * SECTION: MOZILLA UI                                                      *
****************************************************************************/

// PREF: disable Firefox from asking to set as the default browser
user_pref("browser.shell.checkDefaultBrowser", false);

// PREF: disable welcome notices
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.aboutwelcome.enabled", false); // disable Intro screens
 user_pref("startup.homepage_welcome_url", "");
 user_pref("startup.homepage_welcome_url.additional", "");
 user_pref("startup.homepage_override_url", ""); // What's New page after updates


// PREF: new profile switcher
user_pref("browser.profiles.enabled", true);

// PREF: use native title bar buttons [LINUX]
//user_pref("widget.gtk.non-native-titlebar-buttons.enabled", true);

// PREF: disable search engine switcher in the URL bar [FF136+]
// WARNING: Hides "Quick Actions" suggestions.
user_pref("browser.urlbar.scotchBonnet.enableOverride", false);

/****************************************************************************
 * SECTION: THEME ADJUSTMENTS                                              *
****************************************************************************/

// PREF: enable Firefox to use userChome, userContent, etc.
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);

// PREF: add compact mode back to options
user_pref("browser.compactmode.show", true);

// PREF: preferred color scheme for websites
// Dark (0), Light (1), System (2), Browser (3) [DEFAULT FF95+]
user_pref("layout.css.prefers-color-scheme.content-override", 0)

// PREF: prevent private windows being separate from normal windows in taskbar [WINDOWS] [FF106+]
user_pref("browser.privateWindowSeparation.enabled", false);

// PREF: show search bar [FF122+]
// Mozilla has removed the search bar option from the settings window.
user_pref("browser.search.widget.inNavBar", true);

// PREF: new tab page wallpapers
//user_pref("browser.newtabpage.activity-stream.newtabWallpapers.v2.enabled", true); // [DEFAULT FF132+]

// PREF: browser scrollbar styles
// 0 - Default
// 1 - Thin and round, more like Chromium ones
// 2 - Thinner than 1
// 3 - Even thinner than 1
// 4 - Very bold and square
user_pref("widget.non-native-theme.scrollbar.style", 2); // [DEFAULT]

/****************************************************************************
 * SECTION: AI                                                              *
****************************************************************************/
// PREF: AI default controls
user_pref("browser.ai.control.default", "blocked");
user_pref("browser.ml.enable", false);

// PREF: Translations
user_pref("browser.ai.control.translations", "blocked");

// PREF: Chatbot in sidebar
user_pref("browser.ai.control.sidebarChatbot", "blocked");
user_pref("browser.ml.chat.enabled", false);
user_pref("browser.ml.chat.menu", false);

/****************************************************************************
 * SECTION: TRANSLATIONS                                                    *
****************************************************************************/

// PREF: Firefox Translations [FF118+]
user_pref("browser.translations.enable", false); // DEFAULT
user_pref("browser.translations.autoTranslate", false);

/****************************************************************************
 * SECTION: FULLSCREEN NOTICE                                               *
****************************************************************************/

// PREF: remove fullscreen delay
user_pref("full-screen-api.transition-duration.enter", "0 0"); // default=200 200
user_pref("full-screen-api.transition-duration.leave", "0 0"); // default=200 200

// PREF: disable fullscreen notice
// [NOTE] Adjust to a sensible value, like 1250, if you have security concerns.
user_pref("full-screen-api.warning.timeout", 0); // default=3000; alt=1250
user_pref("full-screen-api.warning.delay", -1); // default=500

/****************************************************************************
 * SECTION: FONT APPEARANCE                                                 *
****************************************************************************/

// PREF: smoother font
// [1] 
user_pref("gfx.webrender.quality.force-subpixel-aa-where-possible", true);

// PREF: use DirectWrite everywhere like Chrome [WINDOWS]
user_pref("gfx.font_rendering.cleartype_params.rendering_mode", 5);
user_pref("gfx.font_rendering.cleartype_params.cleartype_level", 100);
user_pref("gfx.font_rendering.cleartype_params.force_gdi_classic_for_families", ""); // DEFAULT FF135+
user_pref("gfx.font_rendering.directwrite.use_gdi_table_loading", false);
 user_pref("gfx.font_rendering.cleartype_params.gamma", 1750);
  user_pref("gfx.font_rendering.cleartype_params.enhanced_contrast", 100);
  user_pref("gfx.font_rendering.cleartype_params.pixel_structure", 1);
	
/****************************************************************************
 * SECTION: URL BAR                                                         *
****************************************************************************/

// PREF: minimize URL bar suggestions (bookmarks, history, open tabs)
// Dropdown options in the URL bar:
user_pref("browser.urlbar.suggest.history", false);
user_pref("browser.urlbar.suggest.bookmark", false); // DEFAULT
user_pref("browser.urlbar.suggest.clipboard", true);
user_pref("browser.urlbar.suggest.openpage",false);
user_pref("browser.urlbar.suggest.engines", true);
user_pref("browser.urlbar.suggest.searches", true);
user_pref("browser.urlbar.quickactions.enabled", true);
user_pref("browser.urlbar.suggest.weather", false); // DEFAULT [FF108]
user_pref("browser.urlbar.weather.ignoreVPN", false); // DEFAULT
user_pref("browser.urlbar.suggest.calculator", false); // [DEFAULT FF137+]
user_pref("browser.urlbar.unitConversion.enabled", false); // [DEFAULT FF141+]

// PREF: disable dropdown suggestions with empty query
user_pref("browser.urlbar.suggest.topsites", false);

// PREF: disable urlbar trending search suggestions [FF118+]
// [SETTING] Search>Search Suggestions>Show trending search suggestions (FF119)
user_pref("browser.urlbar.trending.featureGate", false);
//user_pref("browser.urlbar.suggest.trending", false);

// PREF: disable urlbar suggestions
user_pref("browser.urlbar.addons.featureGate", true); // [FF115+]
user_pref("browser.urlbar.amp.featureGate", false); // [FF141+] adMarketplace
user_pref("browser.urlbar.fakespot.featureGate", false); // [FF130+] [DEFAULT: false]
user_pref("browser.urlbar.mdn.featureGate", false); // [FF117+] [HIDDEN PREF]
user_pref("browser.urlbar.weather.featureGate", false); // [FF108+] [DEFAULT: false]
user_pref("browser.urlbar.wikipedia.featureGate", false); // [FF141+]
user_pref("browser.urlbar.clipboard.featureGate", false); // [FF118+] [DEFAULT: true FF125+]
user_pref("browser.urlbar.yelp.featureGate", false); // [FF124+] [DEFAULT: false]

// PREF: disable recent searches [FF120+]
// [NOTE] Recent searches are cleared with history.
user_pref("browser.urlbar.recentsearches.featureGate", false);

// PREF: disable tab-to-search [FF85+]
// Alternatively, you can exclude on a per-engine basis by unchecking them in Options>Search
// [SETTING] Privacy & Security>Address Bar>When using the address bar, suggest>Search engines
user_pref("browser.urlbar.suggest.engines", true);

// PREF: Adaptive History Autofill
user_pref("browser.urlbar.autoFill", false); // [DEFAULT]
user_pref("browser.urlbar.autoFill.adaptiveHistory.enabled", false);

// PREF: adjust the amount of Address bar / URL bar dropdown results
// This value controls the total number of entries to appear in the location bar dropdown.
// [NOTE] Items (bookmarks/history/openpages) with a high "frequency"/"bonus" will always
// be displayed (no we do not know how these are calculated or what the threshold is),
// and this does not affect the search by search engine suggestion.
// disable=0
user_pref("browser.urlbar.maxRichResults", 6); // default=10

/****************************************************************************
 * SECTION: AUTOPLAY                                                        *
****************************************************************************/

// PREF: do not autoplay media audio
// [NOTE] You can set exceptions under site permissions
// [SETTING] Privacy & Security>Permissions>Autoplay>Settings>Default for all websites
// 0=Allow all, 1=Block non-muted media (default), 5=Block all
user_pref("media.autoplay.default", 1); // DEFAULT
user_pref("media.block-autoplay-until-in-foreground", true); // DEFAULT

// PREF: disable autoplay of HTML5 media if you interacted with the site [FF78+]
// [NOTE] give the website this permission on on neccesery
// 0=sticky (default), 1=transient, 2=user
user_pref("media.autoplay.blocking_policy", 2);

/****************************************************************************
 * SECTION: NEW TAB PAGE                                                    *
****************************************************************************/

// PREF: startup / new tab page
// 0=blank, 1=home, 2=last visited page, 3=resume previous session
// [NOTE] Session Restore is cleared with history and not used in Private Browsing mode
// [SETTING] General>Startup>Open previous windows and tabs
user_pref("browser.startup.page", 1);

// PREF: set HOME+NEW WINDOW page to blank tab
// about:home=Activity Stream, custom URL, about:blank
// [SETTING] Home>New Windows and Tabs>Homepage and new windows
// [Custom URLs] Set two or more websites in Home Page Field – delimited by |
user_pref("browser.startup.homepage", "about:home");

// PREF: set NEWTAB page to blank tab
// true=Firefox Home, false=blank page
// [SETTING] Home>New Windows and Tabs>New tabs
user_pref("browser.newtabpage.enabled", true);

// PREF: Pinned Shortcuts on New Tab
// [SETTINGS] Home>Firefox Home Content
user_pref("browser.newtabpage.activity-stream.discoverystream.enabled", false);
user_pref("browser.newtabpage.activity-stream.showSearch", true); // NTP Web Search [DEFAULT]
user_pref("browser.newtabpage.activity-stream.feeds.topsites", false); // Shortcuts
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false); // Sponsored shortcuts [FF83+]
user_pref("browser.newtabpage.activity-stream.showWeather", false); // Weather [FF130+]
user_pref("browser.newtabpage.activity-stream.system.showWeather", false); // hides Weather as an UI option
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false); // Recommended by Pocket
user_pref("browser.newtabpage.activity-stream.showSponsored", false); // Sponsored stories [FF58+]  
user_pref("browser.newtabpage.activity-stream.showSponsoredCheckboxes", false); // [FF140+] Support Firefox
user_pref("browser.newtabpage.activity-stream.feeds.section.highlights", false); // Recent Activity [DEFAULT]
user_pref("browser.newtabpage.activity-stream.section.highlights.includeBookmarks", false);
user_pref("browser.newtabpage.activity-stream.section.highlights.includeDownloads", false);
user_pref("browser.newtabpage.activity-stream.section.highlights.includeVisited", false);
user_pref("browser.newtabpage.activity-stream.feeds.snippets", false); // [DEFAULT]

// PREF: wallpapers on New Tab [FF128+ NIGHTLY]
user_pref("browser.newtabpage.activity-stream.newtabWallpapers.enabled", false); // Wallpapers

// PREF: clear default topsites
// [NOTE] This does not block you from adding your own.
user_pref("browser.newtabpage.activity-stream.default.sites", "");

// PREF: Firefox logo to always show
user_pref("browser.newtabpage.activity-stream.logowordmark.alwaysVisible", true); // DEFAULT

// PREF: Bookmarks Toolbar visibility
// always, never, or newtab
user_pref("browser.toolbars.bookmarks.visibility", "newtab"); // DEFAULT

/******************************************************************************
 * SECTION: POCKET                                                            *
******************************************************************************/
user_pref("extensions.pocket.enabled", false); // DEFAULT
user_pref("extensions.pocket.api"," ");
user_pref("extensions.pocket.oAuthConsumerKey", " ");
user_pref("extensions.pocket.site", " ");
user_pref("extensions.pocket.showHome", false);

/******************************************************************************
 * SECTION: DOWNLOADS                                 *
******************************************************************************/

// PREF: choose download location
// [SETTING] To set your default "downloads": General>Downloads>Save files to...
// 0=desktop, 1=downloads (default), 2=last used
user_pref("browser.download.folderList", 1); // DEFAULT

// PREF: always ask how to handle new mimetypes [FF101+]
// Enforce user interaction for greater security.
// [SETTING] General>Files and Applications>Applications>What should Firefox do with other files?
// false=Save files
// true=Ask whether to open or save files
user_pref("browser.download.always_ask_before_handling_new_types", true);

// PREF: always ask where to download
// [OPTIONAL HARDENING] Enforce user interaction for greater security.
// [SETTING] General>Files and Applications>Downloads>Always ask you where to save files
// [DIALOGUE] "Ask whether to open or save files"
// true=direct download (default)
// false=the user is asked what to do
user_pref("browser.download.useDownloadDir", false);

// PREF: autohide the downloads button
user_pref("browser.download.autohideButton", true); // DEFAULT

// PREF: disable download panel opening on every download [non-functional?]
user_pref("browser.download.alwaysOpenPanel", false);

// PREF: disable adding downloads to the system's "recent documents" list 
user_pref("browser.download.manager.addToRecentDocs", false);

/****************************************************************************
 * SECTION: TAB BEHAVIOR                                                    *
****************************************************************************/

// PREF: search query opens in a new tab (instead of the current tab)
user_pref("browser.search.openintab", true); // SEARCH BOX
user_pref("browser.urlbar.openintab", true); // URL BAR

// PREF: control behavior of links that would normally open in a new window
// [NOTE] You can still right-click a link and open in a new window
// 3 (default) = in a new tab; pop-up windows are treated like regular tabs
// 2 = in a new window
// 1 = in the current tab
user_pref("browser.link.open_newwindow", 3); // DEFAULT

// PREF: determine the behavior of pages opened by JavaScript (like popups)
// 2 (default) = catch new windows opened by JavaScript that do not have
// specific values set (how large the window should be, whether it
// should have a status bar, etc.) 
// 1 = let all windows opened by JavaScript open in new windows
// 0 = force all new windows opened by JavaScript into tabs
// [NOTE] Most advertising popups also open in new windows with values set
user_pref("browser.link.open_newwindow.restriction", 2); // DEFAULT

// PREF: override <browser.link.open_newwindow> for external links
// Set if a different destination for external links is needed
// 3=Open in a new tab in the current window
// 2=Open in a new window
// 1=Open in the current tab/window
// -1=no overrides (default)
user_pref("browser.link.open_newwindow.override.external", 3); // DEFAULT

// PREF: focus behavior for new tabs from links
// Determine whether a link opens in the foreground or background on left-click
// [SETTINGS] Settings>General>Tabs>"When you open a link, image or media in a new tab, switch to it immediately"
// true(default) = opens new tabs by left-click in the background, leaving focus on the current tab
// false = opens new tabs by left-click in the foreground, putting focus on the new tab
// [NOTE] CTRL+SHIFT+CLICK will open new tabs in foreground (default); switching PREF to false will reverse this behavior
user_pref("browser.tabs.loadInBackground", false); // DEFAULT

// PREF: determines whether pages normally meant to open in a new window (such as
// target="_blank" or from an external program), but that have instead been loaded in a new tab
// This pref takes effect when Firefox has diverted a new window to a new tab instead, then:
// true = loads the new tab in the background, leaving focus on the current tab
// false(default) = loads the new tab in the foreground, taking the focus from the current tab
// [NOTE] Setting this preference to true will still bring the browser to the front when opening links from outside the browser
user_pref("browser.tabs.loadDivertedInBackground", false); // DEFAULT

// PREF: force bookmarks to open in a new tab, not the current tab
user_pref("browser.tabs.loadBookmarksInTabs", true);
user_pref("browser.tabs.loadBookmarksInBackground", true); // load bookmarks in background

// PREF: leave Bookmarks Menu open when selecting a site
user_pref("browser.bookmarks.openInTabClosesMenu", false);

// PREF: show all matches in Findbar
user_pref("findbar.highlightAll", true);

// PREF: disable middle mouse click opening links from clipboard
// It's been default in Linux since at least FF102.
user_pref("middlemouse.contentLoadURL", false);

// PREF: insert new tabs after groups like it
// true(default) = open new tabs to the right of the parent tab
// false = new tabs are opened at the far right of the tab bar
user_pref("browser.tabs.insertRelatedAfterCurrent", true); // DEFAULT

// PREF: insert new tabs immediately after the current tab
user_pref("browser.tabs.insertAfterCurrent", true);

// PREF: enable Tab Previews [FF122+, FF128+]
user_pref("browser.tabs.hoverPreview.enabled", true);
user_pref("browser.tabs.hoverPreview.showThumbnails", true); // DEFAULT
