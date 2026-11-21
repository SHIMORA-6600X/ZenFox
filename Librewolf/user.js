
/****************************************************************************
 * Librewolf                                                                *
 * "SHIMORA"                                                    *
 * version: 160                                                             *
 * url: https://github.com/SHIMORA-6600X/ZenFox                             *
****************************************************************************/

/****************************************************************************
 * SECTION: ZENFOX                                                      *
****************************************************************************/

/** LOADING PAGES ***/
user_pref("nglayout.initialpaint.delay", 20); // DEFAULT; formerly 250
user_pref("nglayout.initialpaint.delay_in_oopif", 20); // DEFAULT
user_pref("gfx.content.skia-font-cache-size", 20); // 20 MB; default=5; Chrome=20
user_pref("content.notify.ontimer", true); // DEFAULT
user_pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s)
user_pref("content.max.tokenizing.time", 1000000); // (1.00s); alt=2000000; HIDDEN
user_pref("content.interrupt.parsing", true); // HIDDEN
user_pref("content.switch.threshold", 500000); // HIDDEN; default= 750000; alt=500000

/** DISK AVOIDANCE ***/
user_pref("browser.cache.disk.enable", false);
user_pref("browser.privatebrowsing.forceMediaMemoryCache", true);
user_pref("media.memory_cache_max_size", 65536);
user_pref("browser.sessionstore.interval", 60000);

/** SPECULATIVE LOADING ***/
user_pref("network.http.speculative-parallel-limit", 0);
user_pref("network.dns.disablePrefetch", true);
user_pref("network.dns.disablePrefetchFromHTTPS", true);
user_pref("browser.urlbar.speculativeConnect.enabled", false);
user_pref("browser.places.speculativeConnect.enabled", false);
user_pref("network.prefetch-next", false);


 /** SECTION: MEMORY CACHE  ***/                                                
user_pref("browser.cache.memory.capacity", 65536); // default=32768 (32 MB)
user_pref("browser.cache.memory.max_entry_size", 10240); // default=5120 (5 MB)
user_pref("browser.sessionhistory.max_total_viewers", -1); // DEFAULT
user_pref("browser.sessionstore.max_tabs_undo", 10); // default=25
user_pref("browser.sessionstore.max_entries", 10); // [HIDDEN OR REMOVED]
user_pref("dom.storage.default_quota", 20480); // 20MB; default=5120
user_pref("dom.storage.shadow_writes", true);


 /** SECTION: GFX RENDERING TWEAKS  ***/
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
user_pref("gfx.canvas.accelerated.cache-items", 1024); // [DEFAULT FF135+]
user_pref("gfx.canvas.accelerated.cache-size", 512); // default=256; Chrome=512; max=2048
user_pref("gfx.canvas.max-size", 65535); // [DEFAULT FF152]

/** SECTION: NETWORK ***/
user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
user_pref("network.buffer.cache.count", 48); // default=24; 128 too large
user_pref("network.http.max-connections", 1800); // default=900
user_pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive
user_pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
user_pref("network.http.max-persistent-connections-per-proxy", 32); // default=32
user_pref("network.http.request.max-start-delay", 5); // default=10
user_pref("network.websocket.max-connections", 200); // DEFAULT

// PREF: increase DNS cache
user_pref("network.dnsCacheEntries", 1600); // [DEFAULT FF152]
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire
user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]
user_pref("network.ssl_tokens_cache_capacity", 8192); // TLS token caching (fast reconnects) [DEFAULT FF152]

// PREF: pacing requests [FF23+]
// false = Firefox will send as many requests as possible without pacing
// true = Firefox will pace requests (default)
user_pref("network.http.pacing.requests.enabled", false);
user_pref("network.http.pacing.requests.min-parallelism", 12); // default=6
user_pref("network.http.pacing.requests.burst", 20); // default=10

 /** SECTION: TAB UNLOAD  ***/

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


 /** SECTION: DISK CACHE  ***/
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
 * SECTION: LITEFOX                                                       *
****************************************************************************/

/** NEW TAB PAGE ***/
// 0=blank, 1=home, 2=last visited page, 3=resume previous session
user_pref("browser.startup.page", 1);

// true=Firefox Home, false=blank page
user_pref("browser.newtabpage.enabled", true);

/** TAB BEHAVIOR ***/
user_pref("browser.search.openintab", false); // SEARCH BOX
user_pref("browser.urlbar.openintab", false); // URL BAR
user_pref("browser.link.open_newwindow", 2); // DEFAULT

// 3=Open in a new tab in the current window
// 2=Open in a new window
// 1=Open in the current tab/window
// -1=no overrides (default)
user_pref("browser.link.open_newwindow.override.external", 2); // DEFAULT

// PREF: show all matches in Findbar
user_pref("findbar.highlightAll", true);

// PREF: disable middle mouse click opening links from clipboard
user_pref("middlemouse.contentLoadURL", false);

// PREF: do not hide the pointer while typing [LINUX]
user_pref("widget.gtk.hide-pointer-while-typing.enabled", false);

// PREF: enable Tab Previews [FF122+, FF128+]
user_pref("browser.tabs.hoverPreview.enabled", true);
user_pref("browser.tabs.hoverPreview.showThumbnails", true); // DEFAULT

/** SEARCH / URL BAR ***/
user_pref("browser.urlbar.trimHttps", true);
user_pref("browser.urlbar.untrimOnUserInteraction.featureGate", true);
user_pref("browser.search.separatePrivateDefault.ui.enabled", true);
user_pref("browser.search.suggest.enabled", true);
user_pref("browser.urlbar.quicksuggest.enabled", false);
user_pref("browser.urlbar.groupLabels.enabled", false);
user_pref("browser.formfill.enable", false);
user_pref("network.IDN_show_punycode", true);

/** PASSWORDS ***/
user_pref("signon.formlessCapture.enabled", false);
user_pref("signon.privateBrowsingCapture.enabled", false);
user_pref("network.auth.subresource-http-auth-allow", 1);
user_pref("editor.truncate_user_pastes", false);


/** MOZILLA UI ***/
user_pref("extensions.getAddons.showPane", false);
user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);
user_pref("browser.discovery.enabled", false);
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", false);
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", false);
user_pref("browser.preferences.moreFromMozilla", false);
user_pref("browser.aboutConfig.showWarning", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.aboutwelcome.enabled", false);
user_pref("browser.profiles.enabled", true);

/** THEME ADJUSTMENTS ***/
user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);
user_pref("browser.compactmode.show", true);
user_pref("browser.privateWindowSeparation.enabled", false); // WINDOWS

// PREF: preferred color scheme for websites
// Dark (0), Light (1), System (2), Browser (3) [DEFAULT FF95+]
user_pref("layout.css.prefers-color-scheme.content-override", 0);
user_pref("browser.privateWindowSeparation.enabled", false);

/** URL BAR ***/
user_pref("browser.urlbar.trending.featureGate", false);

/** NEW TAB PAGE ***/
user_pref("browser.newtabpage.activity-stream.default.sites", "");
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.showSponsored", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredCheckboxes", false);

/** DOWNLOADS ***/
user_pref("browser.download.manager.addToRecentDocs", false);

/** PDF ***/
user_pref("browser.download.open_pdf_attachments_inline", true);

/** TAB BEHAVIOR ***/
user_pref("browser.bookmarks.openInTabClosesMenu", false);
user_pref("browser.menu.showViewImageInfo", true);
user_pref("findbar.highlightAll", true);
user_pref("layout.word_select.eat_space_to_next_word", false);

/****************************************************************************
 * SECTION: ADVANCEDFOX                                                     *
****************************************************************************/

/** TELEMETRY ***/
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("toolkit.telemetry.unified", false);
user_pref("toolkit.telemetry.enabled", false);
user_pref("toolkit.telemetry.server", "data:,");
user_pref("toolkit.telemetry.archive.enabled", false);
user_pref("toolkit.telemetry.newProfilePing.enabled", false);
user_pref("toolkit.telemetry.shutdownPingSender.enabled", false);
user_pref("toolkit.telemetry.updatePing.enabled", false);
user_pref("toolkit.telemetry.bhrPing.enabled", false);
user_pref("toolkit.telemetry.firstShutdownPing.enabled", false);
user_pref("toolkit.telemetry.coverage.opt-out", true);
user_pref("toolkit.coverage.opt-out", true);
user_pref("toolkit.coverage.endpoint.base", "");
user_pref("browser.newtabpage.activity-stream.feeds.telemetry", false);
user_pref("browser.newtabpage.activity-stream.telemetry", false);
user_pref("datareporting.usage.uploadEnabled", false);

/** CRASH REPORTS ***/
user_pref("breakpad.reportURL", "");
user_pref("browser.tabs.crashReporting.sendReport", false);

/** HTTPS-ONLY MODE ***/
user_pref("dom.security.https_only_mode", true);
user_pref("dom.security.https_only_mode_error_page_user_suggestions", true);

/** SAFE BROWSING ***/
user_pref("browser.safebrowsing.downloads.remote.enabled", false);

/****************************************************************************
 * SECTION: SOFTFOX                                                       *
****************************************************************************/

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
user_pref("mousewheel.default.delta_multiplier_y", 240);

/****************************************************************************
 * END: ZENFOX*
****************************************************************************/
