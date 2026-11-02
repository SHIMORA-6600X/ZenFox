
/****************************************************************************************
 * SmartFox                                                                             *
 * "SHIMORA"                                                                     *
 * priority: Better Browsing                                                           *
 * version: 157                                                                         *
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

// PREF: Font rendering cache in Skia (32MB)
user_pref("gfx.content.skia-font-cache-size", 20); // 20 MB; default=5; Chrome=20

// PREF: page reflow timer
// true = do not reflow pages at an interval any higher than that specified by content.notify.interval (default)
// false = reflow pages whenever new data is received
user_pref("content.notify.ontimer", true); // DEFAULT

// PREF: content notification delay - notification interval (in microseconds) to avoid layout thrashing
user_pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s)
user_pref("content.max.tokenizing.time", 1000000); // (1.00s); alt=2000000; HIDDEN
user_pref("content.interrupt.parsing", true); // HIDDEN

// PREF: UI responsiveness threshold
user_pref("content.switch.threshold", 500000); // HIDDEN; default= 750000; alt=500000

// PREF: new tab preload
user_pref("browser.newtab.preload", true); // DEFAULT

// PREF: disable EcoQoS [WINDOWS]
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
user_pref("gfx.webrender.all", true); // enables WR + additional features
user_pref("gfx.webrender.precache-shaders", true); // longer initial startup time
user_pref("gfx.webrender.compositor", true); // DEFAULT WINDOWS macOS
user_pref("gfx.webrender.compositor.force-enabled", true); // enforce

// PREF: Webrender layer compositor
user_pref("gfx.webrender.layer-compositor", true); // [DEFAULT FF152]

// PREF: improve CPU usage on AMD systems
user_pref("media.wmf.zero-copy-nv12-textures-force-enabled", true);

// PREF: if your hardware doesn't support Webrender, you can fallback to Webrender's software renderer
// Note: If you using Linux Enable This Options 
//user_pref("gfx.webrender.software", true); // Software Webrender uses CPU instead of GPU
    //user_pref("gfx.webrender.software.opengl", true); // LINUX

// PREF: GPU-accelerated Canvas2D
// increase GPU Performance 
user_pref("gfx.canvas.accelerated", true); // [DEFAULT FF133+]
user_pref("gfx.canvas.accelerated.cache-items", 4096); // [DEFAULT FF135+]
user_pref("gfx.canvas.accelerated.cache-size", 512); // default=256; Chrome=512; max=2048 [4]
user_pref("gfx.canvas.max-size", 65535); // [DEFAULT FF152]

/****************************************************************************
 * SECTION: JAVASCRIPT OPTIONS                                              *
****************************************************************************/
// PREF: lower the Baseline JIT compilation threshold
// Controls how many times a function runs before Firefox promotes it from the
// C++ interpreter to the Baseline JIT compiler. The Baseline JIT compiles each
// bytecode instruction into a small piece of machine code and uses Inline Caches
// (ICs) to both speed up execution and collect type info for the Ion optimizing JIT.
// Lowering this from 100 to 50 promotes "warm" functions to compiled machine code
// sooner, which reduces dropped frames while browsing.
user_pref("javascript.options.baselinejit.threshold", 50); // default=100

// PREF: raise the IonMonkey (Ion) optimizing-JIT compilation threshold
user_pref("javascript.options.ion.threshold", 1500); // DEFAULT

// PREF: decrease concurrent JavaScript garbage collection (GC) threads
// Sets the divisor in the formula: GC threads = CPU threads ÷ divisor (min 1).
// A LOWER value = MORE parallel GC threads. A HIGHER value = FEWER threads.
// Example (24-thread CPU):  divisor 1 → 24 threads | 2 → 12 | 4 (default) → 6 | 12 → 2
// Power users with many cores should LOWER this value, not raise it.
// [NOTE] Mozilla's default of 4 is conservative to avoid thread contention on weak hardware.
user_pref("javascript.options.concurrent_multiprocess_gcs.cpu_divisor", 2); // DEFAULT

/****************************************************************************
 * SECTION: DISK CACHE                                                     *
****************************************************************************/

// PREF: force a fixed max cache size on disk
user_pref("browser.cache.disk.smart_size.enabled", false);

// PREF: disk cache size
user_pref("browser.cache.disk.capacity", 512000); // default=256000; size of disk cache; 1024000=1GB, 2048000=2GB
user_pref("browser.cache.disk.max_entry_size", 51200); // DEFAULT (50 MB); maximum size of an object in disk cache

// PREF: cache memory pool
user_pref("browser.cache.disk.metadata_memory_limit", 1024); // DEFAULT (1 MB); limit of recent metadata we keep in memory for faster access

// PREF: number of chunks we preload ahead of read
user_pref("browser.cache.disk.preload_chunk_count", 8); // default=4

// PREF: the time period used to re-compute the frecency value of cache entries
user_pref("browser.cache.frecency_half_life_hours", 6); // DEFAULT

// PREF: memory limit (in kB) for new cache data not yet written to disk
user_pref("browser.cache.disk.max_chunks_memory_usage", 40960); // DEFAULT (40 MB)
user_pref("browser.cache.disk.max_priority_chunks_memory_usage", 40960); // DEFAULT (40 MB)

// PREF: how often to validate document in cache
// 0 = once-per-session
// 1 = each-time
// 2 = never
// 3 = when-appropriate/automatically (default)
user_pref("browser.cache.check_doc_frequency", 3); // DEFAULT

// PREF: enforce free space checks
user_pref("browser.cache.disk.free_space_soft_limit", 10240); // default=5120 (5 MB)
user_pref("browser.cache.disk.free_space_hard_limit", 2048); // default=1024 (1 MB)

// PREF: compression level for cached JavaScript bytecode [FF102+]
// 0 = do not compress (default)
// 1 = minimal compression
// 9 = maximal compression
user_pref("browser.cache.jsbc_compression_level", 1);

/****************************************************************************
 * SECTION: MEMORY CACHE                                                   *
****************************************************************************/

// PREF: memory cache
// For machines with 8GB+ RAM, that equals 32768 kb = 32 MB
user_pref("browser.cache.memory.capacity", 65536); // default=32768 (32 MB)
user_pref("browser.cache.memory.max_entry_size", 10240); // default=5120 (5 MB)

// PREF: amount of Back/Forward cached pages stored in memory for each tab
user_pref("browser.sessionhistory.max_total_viewers", -1); // DEFAULT
user_pref("browser.sessionstore.max_tabs_undo", 10); // default=25
user_pref("browser.sessionstore.max_entries", 10); // [HIDDEN OR REMOVED]
user_pref("dom.storage.default_quota", 20480); // 20MB; default=5120
user_pref("dom.storage.shadow_writes", true);

// PREF: tell garbage collector to start running when javascript is using xx MB of memory
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
user_pref("media.cache_readahead_limit", 3600); // 60 min; default=60 sec; stop reading ahead when our buffered data is this many seconds ahead of the current playback
user_pref("media.cache_resume_threshold", 1800); // 30 min; default=30 sec; when a network connection is suspended, don't resume it until the amount of buffered data falls below this threshold

/****************************************************************************
 * SECTION: IMAGE CACHE                                                     *
****************************************************************************/

// PREF: image cache
user_pref("image.cache.size", 20971520); // (cache images up to 20 MiB in size) [DEFAULT]
user_pref("image.mem.decode_bytes_at_a_time", 32768); // default=16384; chunk size for calls to the image decoders
user_pref("image.mem.max_decoded_image_kb", 512000); // 500MB [HIDDEN OR REMOVED?]

// PREF: set minimum timeout to unmap shared surfaces since they have been last used
// [NOTE] This is only used on 32-bit builds of Firefox where there is meaningful
// virtual address space pressure.
user_pref("image.mem.shared.unmap.min_expiration_ms", 120000); // default=60000; minimum timeout to unmap shared surfaces since they have been last used

/****************************************************************************
 * SECTION: NETWORK                                                         *
****************************************************************************/

// PREF: use bigger packets
// [WARNING] Cannot open HTML files bigger than 4MB if value is too large [2].
// Reduce Firefox's CPU usage by requiring fewer application-to-driver data transfers.
// However, it does not affect the actual packet sizes transmitted over the network.
user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
user_pref("network.buffer.cache.count", 48); // default=24; 128 too large

// PREF: increase the absolute number of HTTP connections
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
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire

// PREF: the number of threads for DNS
user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]

// PREF: increase TLS token caching 
user_pref("network.ssl_tokens_cache_capacity", 8192); // TLS token caching (fast reconnects) [DEFAULT FF152]

/****************************************************************************
 * SECTION: TAB UNLOAD                                                      *
****************************************************************************/

// PREF: unload tabs on low memory
user_pref("browser.tabs.unloadOnLowMemory", true); // DEFAULT

// PREF: determine when tabs unload [WINDOWS] [LINUX]
// Set this to some value, e.g. 4/5 of total memory available on your system:
// 4GB=3276, 8GB=6553, 16GB=13107, 32GB=25698, 64GB=52429
user_pref("browser.low_commit_space_threshold_mb",6553); // default=200; WINDOWS LINUX

// PREF: determine when tabs unload [LINUX]
user_pref("browser.low_commit_space_threshold_percent", 5); // default=5; LINUX

// PREF: determine how long (in ms) tabs are inactive before they unload
// 60000=1min; 300000=5min; 600000=10min (default)
user_pref("browser.tabs.min_inactive_duration_before_unload", 300000); // 5min; default=600000

/****************************************************************************
 * SECTION: PROCESS COUNT                                                  *
****************************************************************************/

user_pref("dom.ipc.keepProcessesAlive.web", 4); // default=1 [HIDDEN OR REMOVED]

// PREF: use one process for process preallocation cache
user_pref("dom.ipc.processPrelaunch.fission.number", 1); // default=3; Process Preallocation Cache

// PREF: configure process isolation
// Note: isolate the high value web
user_pref("fission.webContentIsolationStrategy", 2);
user_pref("browser.preferences.defaultPerformanceSettings.enabled", false);
user_pref("dom.ipc.processCount.webIsolated", 1); // one process per site origin (high value)
user_pref("dom.ipc.processCount", 8); // determine by number of CPU cores/processors


/****************************************************************************************
 * SECTION: LITEFOX                                   *
 ****************************************************************************************/

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
user_pref("layout.css.prefers-color-scheme.content-override", 0);

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
// [SECURITY v157] Safe defaults kept (1250/500). Setting 0/-1 removes anti-spoofing
// protection and is opt-in only for trusted kiosk setups.
user_pref("full-screen-api.warning.timeout", 1250); // default=3000; unsafe opt-in=0
user_pref("full-screen-api.warning.delay", 500); // default=500; unsafe opt-in=-1

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
// [NOTE] browser.urlbar.suggest.engines already set to true above (deduped v157).

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
// [REMOVED v157] Pocket was removed from modern Firefox; these prefs are dead.
// Kept commented for ESR reference only.
//user_pref("extensions.pocket.enabled", false); // DEFAULT
//user_pref("extensions.pocket.api"," ");
//user_pref("extensions.pocket.oAuthConsumerKey", " ");
//user_pref("extensions.pocket.site", " ");
//user_pref("extensions.pocket.showHome", false);

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
user_pref("browser.search.openintab", false); // SEARCH BOX
user_pref("browser.urlbar.openintab", false); // URL BAR

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



/****************************************************************************************
 * SECTION: SOFTFOX                                    *
 ****************************************************************************************/



/****************************************************************************************
 * OPTION: ZEN SMOOTH SCROLLING [ACTIVE - DEFAULT]                                    *
 ****************************************************************************************/
// recommended for 120hz+ displays
user_pref("general.smoothScroll.msdPhysics.enabled", true);
user_pref("general.smoothScroll.currentVelocityWeighting", "0.15");
user_pref("general.smoothScroll.stopDecelerationWeighting", "0.6");
user_pref("mousewheel.min_line_scroll_amount", 10);
user_pref("general.smoothScroll.mouseWheel.durationMinMS", 80);
user_pref("general.smoothScroll.msdPhysics.continuousMotionMaxDeltaMS", 12);
user_pref("general.smoothScroll.msdPhysics.motionBeginSpringConstant", 600);
user_pref("general.smoothScroll.msdPhysics.regularSpringConstant", 650);
user_pref("general.smoothScroll.msdPhysics.slowdownMinDeltaMS", 25);
user_pref("general.smoothScroll.msdPhysics.slowdownSpringConstant", 250);
user_pref("mousewheel.default.delta_multiplier_y", 210);
