/****************************************************************************************
 * ZenFox                                                                             *
 * "SHIMORA"                                                                     *
 * priority: Better browsing                                                            *
 * version: 155                                                                         *
 * url: https://github.com/SHIMORA-6600X/ZenFox                                       *
 ***************************************************************************************/

/****************************************************************************
 * SECTION: GENERAL                                                        *
****************************************************************************/

// PREF: initial paint delay
// How long FF will wait before rendering the page (in ms)
// [NOTE] You may prefer using 250.
// [NOTE] Dark Reader users may want to use 1000 [3].
user_pref("nglayout.initialpaint.delay", 10); // DEFAULT; formerly 250
user_pref("nglayout.initialpaint.delay_in_oopif", 10); // DEFAULT
user_pref("gfx.content.skia-font-cache-size", 20); // 20 MB; default=5; Chrome=20
user_pref("content.notify.ontimer", true); // DEFAULT
user_pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s)
user_pref("content.max.tokenizing.time", 1000000); // (1.00s); alt=2000000; HIDDEN
user_pref("content.interrupt.parsing", true); // HIDDEN
user_pref("content.switch.threshold", 300000); // HIDDEN; default= 750000; alt=500000

// PREF: new tab preload
// [WARNING] Disabling this may cause a delay when opening a new tab in Firefox.
user_pref("browser.newtab.preload", true); // DEFAULT
user_pref("dom.ipc.processPriorityManager.backgroundUsesEcoQoS", false);

// PREF: control how tabs are loaded when a session is restored
// true=Tabs are not loaded until they are selected (default)
// false=Tabs begin to load immediately.
user_pref("browser.sessionstore.restore_on_demand", true); // DEFAULT
user_pref("browser.sessionstore.restore_pinned_tabs_on_demand", true);
user_pref("browser.sessionstore.restore_tabs_lazily", true); // DEFAULT

// PREF: disable preSkeletonUI on startup [WINDOWS]
user_pref("browser.startup.preXulSkeletonUI", false);

/****************************************************************************
 * SECTION: GFX RENDERING TWEAKS                                            *
****************************************************************************/

// PREF: Webrender tweaks
// Webrender will Make Firefox Using GPU To Optmize CPU Usage & You Got a Smooth Animation  and Best browsing experience
user_pref("gfx.webrender.all", true); // enables WR + additional features
user_pref("gfx.webrender.precache-shaders", true); // longer initial startup time
user_pref("gfx.webrender.compositor", true); // DEFAULT WINDOWS macOS
user_pref("gfx.webrender.compositor.force-enabled", true); // enforce
user_pref("gfx.webrender.layer-compositor", true); // [DEFAULT FF152]

// PREF: improve CPU usage on AMD systems
// That's Better option for Amd CPU's I Recommended to enable it 
user_pref("media.wmf.zero-copy-nv12-textures-force-enabled", true);
user_pref("gfx.canvas.accelerated", true); // [DEFAULT FF133+]
user_pref("gfx.canvas.accelerated.cache-items", 2048); // [DEFAULT FF135+]
user_pref("gfx.canvas.accelerated.cache-size", 512); // default=256; Chrome=512; max=2048
user_pref("gfx.canvas.max-size", 65535); // [DEFAULT FF152]

/****************************************************************************
 * SECTION: JAVASCRIPT OPTIONS                                              *
****************************************************************************/
user_pref("javascript.options.baselinejit.threshold", 50); // default=100
user_pref("javascript.options.ion.threshold", 1500); // DEFAULT
/****************************************************************************
 * SECTION: DISK CACHE                                                     *
****************************************************************************/
user_pref("browser.cache.disk.smart_size.enabled", false);
user_pref("browser.cache.disk.capacity", 1024000); // default=256000; size of disk cache; 1024000=1GB, 2048000=2GB
user_pref("browser.cache.disk.max_entry_size", 51200); // DEFAULT (50 MB); maximum size of an object in disk cache
user_pref("browser.cache.disk.metadata_memory_limit", 1024); // DEFAULT (1 MB); limit of recent metadata we keep in memory for faster access
user_pref("browser.cache.disk.preload_chunk_count", 8); // default=4
user_pref("browser.cache.frecency_half_life_hours", 6); // DEFAULT
user_pref("browser.cache.disk.max_chunks_memory_usage", 40960); // DEFAULT (40 MB)
user_pref("browser.cache.disk.max_priority_chunks_memory_usage", 40960); // DEFAULT (40 MB)

// PREF: how often to validate document in cache
// 0 = once-per-session
// 1 = each-time
// 2 = never
// 3 = when-appropriate/automatically (default)
user_pref("browser.cache.check_doc_frequency", 3); // DEFAULT
user_pref("browser.cache.disk.free_space_soft_limit", 10240); // default=5120 (5 MB)
user_pref("browser.cache.disk.free_space_hard_limit", 2048); // default=1024 (1 MB)

// PREF: compression level for cached JavaScript bytecode [FF102+]
// 0 = do not compress (default)
// 1 = minimal compression
// 9 = maximal compression
user_pref("browser.cache.jsbc_compression_level", 1);
user_pref("dom.script_loader.bytecode_cache.enabled", true); // DEFAULT
user_pref("dom.script_loader.bytecode_cache.strategy", 0); // DEFAULT

/****************************************************************************
 * SECTION: MEMORY CACHE                                                   *
****************************************************************************/

// PREF: memory cache
user_pref("browser.cache.memory.capacity", 65536); // default=32768 (32 MB)
user_pref("browser.cache.memory.max_entry_size", 10240); // default=5120 (5 MB)
user_pref("browser.sessionhistory.max_total_viewers", -1); // DEFAULT
user_pref("browser.sessionstore.max_tabs_undo", 10); // default=25
user_pref("browser.sessionstore.max_entries", 10); // [HIDDEN OR REMOVED]
user_pref("dom.storage.default_quota", 20480); // 20MB; default=5120
user_pref("dom.storage.shadow_writes", true);

// PREF: tell garbage collector to start running when javascript is using xx MB of memory
// Garbage collection releases memory back to the system.
user_pref("javascript.options.mem.high_water_mark", 128); // DEFAULT [HIDDEN OR REMOVED]

/****************************************************************************
 * SECTION: MEDIA CACHE                                                     *
****************************************************************************/

// PREF: media disk cache
user_pref("media.cache_size", 512000); // DEFAULT

// PREF: media cache combine sizes
user_pref("media.memory_caches_combined_limit_kb", 1048576); // 1GB; default=524288
user_pref("media.memory_caches_combined_limit_pc_sysmem", 5); // DEFAULT; alt=10; the percentage of system memory that Firefox can use for media caches

// PREF: Media Source Extensions (MSE) web standard
// Disabling MSE allows videos to fully buffer, but you're limited to 720p.
// [WARNING] Disabling MSE may break certain videos.
// false=Firefox plays the old WebM format
// true=Firefox plays the new WebM format (default)
user_pref("media.mediasource.enabled", true); // DEFAULT

// PREF: adjust video buffering periods when not using MSE (in seconds)
// [NOTE] Does not affect videos over 720p since they use DASH playback [1] or Web Audio API
user_pref("media.cache_readahead_limit", 3600); // 60 min; default=60 sec; stop reading ahead when our buffered data is this many seconds ahead of the current playback
user_pref("media.cache_resume_threshold", 1800); // 30 min; default=30 sec; when a network connection is suspended, don't resume it until the amount of buffered data falls below this threshold

/****************************************************************************
 * SECTION: IMAGE CACHE                                                     *
****************************************************************************/

// PREF: image cache
user_pref("image.cache.size", 20971520); // (cache images up to 20 MiB in size) [DEFAULT]
user_pref("image.mem.decode_bytes_at_a_time", 32768); // default=16384; chunk size for calls to the image decoders
user_pref("image.mem.max_decoded_image_kb", 512000); // 500MB [HIDDEN OR REMOVED?]

/****************************************************************************
 * SECTION: NETWORK                                                         *
****************************************************************************/

// PREF: use bigger packets
// [WARNING] Cannot open HTML files bigger than 4MB if value is too large [2].
// Reduce Firefox's CPU usage by requiring fewer application-to-driver data transfers.
// However, it does not affect the actual packet sizes transmitted over the network.
user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
user_pref("network.buffer.cache.count", 48); // default=24; 128 too large
user_pref("network.http.max-connections", 1800); // default=900
user_pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive
user_pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
user_pref("network.http.max-persistent-connections-per-proxy", 32); // default=32
user_pref("network.http.request.max-start-delay", 5); // default=10
user_pref("network.websocket.max-connections", 200); // DEFAULT

// PREF: pacing requests [FF23+]
// false = Firefox will send as many requests as possible without pacing
// true = Firefox will pace requests (default)
user_pref("network.http.pacing.requests.enabled", false);
user_pref("network.http.pacing.requests.min-parallelism", 12); // default=6
user_pref("network.http.pacing.requests.burst", 20); // default=10

// PREF: increase DNS cache
user_pref("network.dnsCacheEntries", 1600); // [DEFAULT FF152]

// PREF: adjust DNS expiration time
// [ABOUT] about:networking#dns
// [NOTE] These prefs will be ignored by DNS resolver if using DoH/TRR.
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire
user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]
user_pref("network.ssl_tokens_cache_capacity", 8192); // TLS token caching (fast reconnects) [DEFAULT FF152]

/****************************************************************************
 * SECTION: TAB UNLOAD                                                      *
****************************************************************************/

// PREF: unload tabs on low memory
user_pref("browser.tabs.unloadOnLowMemory", true); // DEFAULT

// 4GB=3276, 8GB=6553, 16GB=13107, 32GB=25698, 64GB=52429
user_pref("browser.low_commit_space_threshold_mb", 3276); // default=200; WINDOWS LINUX

// PREF: determine when tabs unload [LINUX]
// Yeah I know i disable this option beacause i don't wanna any issue if you Using Windows But if you are on Linux you can enable it 
// On Linux, Firefox checks available memory in comparison to total memory,
// and use this percent value (out of 100) to determine if Firefox is in a
// low memory scenario.
//user_pref("browser.low_commit_space_threshold_percent", 5); // default=5; LINUX

// PREF: determine how long (in ms) tabs are inactive before they unload
// 60000=1min; 300000=5min; 600000=10min (default)
user_pref("browser.tabs.min_inactive_duration_before_unload", 300000); // 5min; default=600000

/****************************************************************************
 * SECTION: PROCESS COUNT                                                  *
****************************************************************************/

// PREF: process count
// [ABOUT] View in about:processes.
// With Firefox Quantum (2017), CPU cores = processCount. However, since the
// introduction of Fission [2], the number of website processes is controlled
// by processCount.webIsolated. Disabling fission.autostart or changing
// fission.webContentIsolationStrategy reverts control back to processCount.
user_pref("dom.ipc.processCount", 8); // DEFAULT; Shared Web Content
user_pref("dom.ipc.processCount.webIsolated", 1); // default=4; Isolated Web Content
user_pref("dom.ipc.keepProcessesAlive.web", 4); // default=1 [HIDDEN OR REMOVED]

// PREF: use one process for process preallocation cache
user_pref("dom.ipc.processPrelaunch.fission.number", 1); // default=3; Process Preallocation Cache

// OPTION 2: isolate only "high value" websites
// Only isolates web content loaded by sites which are considered "high
// value". A site is considered high value if it has been granted a
// `highValue*` permission by the permission manager, which is done in
// response to certain actions.
user_pref("fission.webContentIsolationStrategy", 2);
user_pref("browser.preferences.defaultPerformanceSettings.enabled", false);
user_pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin (high value)
user_pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors

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

// PREF: disable "What's New" toolbar icon [FF69+]
//user_pref("browser.messaging-system.whatsNewPanel.enabled", false);

// PREF: new profile switcher
user_pref("browser.profiles.enabled", true);

// PREF: use native title bar buttons [LINUX]
user_pref("widget.gtk.non-native-titlebar-buttons.enabled", true);
user_pref("browser.tabs.firefox-view", true);
/****************************************************************************
 * SECTION: THEME ADJUSTMENTS                                              *
****************************************************************************/

user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.compactmode.show", true);

// PREF: preferred color scheme for websites
// Dark (0), Light (1), System (2), Browser (3) [DEFAULT FF95+]
user_pref("layout.css.prefers-color-scheme.content-override", 0);
user_pref("browser.privateWindowSeparation.enabled", false);

// PREF: show search bar [FF122+]
// Mozilla has removed the search bar option from the settings window.
user_pref("browser.search.widget.inNavBar", true);

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

// PREF: Key points in link previews
user_pref("browser.ai.control.linkPreviewKeyPoints", "blocked");
user_pref("browser.ml.linkPreview.enabled", false);

// PREF: Chatbot in sidebar
user_pref("browser.ai.control.sidebarChatbot", "blocked");
user_pref("browser.ml.chat.enabled", false);
user_pref("browser.ml.chat.menu", false);

/****************************************************************************
 * SECTION: TRANSLATIONS                                                    *
****************************************************************************/

// PREF: Firefox Translations [FF118+]
// Automated translation of web content is done locally in Firefox, so that
// the text being translated does not leave your machine.
// [ABOUT] Visit about:translations to translate your own text as well.
user_pref("browser.translations.enable", true); // DEFAULT
user_pref("browser.translations.autoTranslate", true);

/****************************************************************************
 * SECTION: FULLSCREEN NOTICE                                               *
****************************************************************************/

// PREF: remove fullscreen delay
user_pref("full-screen-api.transition-duration.enter", "0 0"); // default=200 200
user_pref("full-screen-api.transition-duration.leave", "0 0"); // default=200 200
/****************************************************************************
 * SECTION: FONT APPEARANCE                                                 *
****************************************************************************/

// PREF: smoother font
user_pref("gfx.webrender.quality.force-subpixel-aa-where-possible", true);

// PREF: use DirectWrite everywhere like Chrome [WINDOWS]
user_pref("gfx.font_rendering.cleartype_params.rendering_mode", 5);
user_pref("gfx.font_rendering.cleartype_params.cleartype_level", 100);
user_pref("gfx.font_rendering.cleartype_params.force_gdi_classic_for_families", ""); // DEFAULT FF135+
user_pref("gfx.font_rendering.directwrite.use_gdi_table_loading", false);
// Some users find these helpful:
   user_pref("gfx.font_rendering.cleartype_params.gamma", 1750);
    user_pref("gfx.font_rendering.cleartype_params.enhanced_contrast", 100);
    user_pref("gfx.font_rendering.cleartype_params.pixel_structure", 1);

/****************************************************************************
 * SECTION: URL BAR                                                         *
****************************************************************************/
user_pref("browser.urlbar.autoFill", true); // [DEFAULT]
user_pref("browser.urlbar.maxRichResults", 5); // default=10

/****************************************************************************
 * SECTION: AUTOPLAY                                                        *
****************************************************************************/

// PREF: do not autoplay media audio
// [NOTE] You can set exceptions under site permissions
// [SETTING] Privacy & Security>Permissions>Autoplay>Settings>Default for all websites
// 0=Allow all, 1=Block non-muted media (default), 5=Block all
user_pref("media.autoplay.default", 1); // DEFAULT
user_pref("media.block-autoplay-until-in-foreground", true); // DEFAULT

/****************************************************************************
 * SECTION: NEW TAB PAGE                                                    *
****************************************************************************/

// PREF: startup / new tab page
// 0=blank, 1=home, 2=last visited page, 3=resume previous session
user_pref("browser.startup.page", 1);
// PREF: set NEWTAB page to blank tab
// true=Firefox Home, false=blank page
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

/******************************************************************************
 * SECTION: POCKET                                                            *
******************************************************************************/

// PREF: disable built-in Pocket extension
user_pref("extensions.pocket.enabled", false); // DEFAULT
user_pref("extensions.pocket.api"," ");
user_pref("extensions.pocket.oAuthConsumerKey", " ");
user_pref("extensions.pocket.site", " ");
user_pref("extensions.pocket.showHome", false);

/******************************************************************************
 * SECTION: DOWNLOADS                                 *
******************************************************************************/
user_pref("browser.download.folderList", 1); // DEFAULT
user_pref("browser.download.always_ask_before_handling_new_types", true);
user_pref("browser.download.useDownloadDir", false);
user_pref("browser.download.autohideButton", true); // DEFAULT
user_pref("browser.download.alwaysOpenPanel", false);
user_pref("browser.download.manager.addToRecentDocs", false);

/****************************************************************************
 * SECTION: TAB BEHAVIOR                                                    *
****************************************************************************/
user_pref("browser.search.openintab", false); // SEARCH BOX
user_pref("browser.urlbar.openintab", false); // URL BAR
user_pref("browser.link.open_newwindow", 2); // DEFAULT

// PREF: override <browser.link.open_newwindow> for external links
// Set if a different destination for external links is needed
// 3=Open in a new tab in the current window
// 2=Open in a new window
// 1=Open in the current tab/window
// -1=no overrides (default)
user_pref("browser.link.open_newwindow.override.external", 2); // DEFAULT

// PREF: force bookmarks to open in a new tab, not the current tab
user_pref("browser.tabs.loadBookmarksInTabs", true);
user_pref("browser.tabs.loadBookmarksInBackground", true); // load bookmarks in background

// PREF: leave Bookmarks Menu open when selecting a site
user_pref("browser.bookmarks.openInTabClosesMenu", false);

// PREF: show all matches in Findbar
user_pref("findbar.highlightAll", true);


// PREF: disable middle mouse click opening links from clipboard
user_pref("middlemouse.contentLoadURL", false);

// PREF: do not hide the pointer while typing [LINUX]
user_pref("widget.gtk.hide-pointer-while-typing.enabled", false);

// PREF: enable Tab Previews [FF122+, FF128+]
user_pref("browser.tabs.hoverPreview.enabled", true);
user_pref("browser.tabs.hoverPreview.showThumbnails", true); // DEFAULT

/****************************************************************************************
 * OPTION: SHARPEN SCROLLING                                                           *
****************************************************************************************/
// only sharpen scrolling
user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
user_pref("general.smoothScroll", true); // DEFAULT
user_pref("mousewheel.min_line_scroll_amount", 10); // adjust this number to your liking; default=5
user_pref("general.smoothScroll.mouseWheel.durationMinMS", 80); // default=50
user_pref("general.smoothScroll.currentVelocityWeighting", "0.15"); // default=.25
user_pref("general.smoothScroll.stopDecelerationWeighting", "0.6"); // default=.4

/****************************************************************************************
 * OPTION: SMOOTH SCROLLING                                                            *
****************************************************************************************/
// recommended for 90hz+ displays
user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
user_pref("general.smoothScroll", true); // DEFAULT
user_pref("general.smoothScroll.msdPhysics.enabled", true);
user_pref("mousewheel.default.delta_multiplier_y", 300); // 250-400; adjust this number to your liking
