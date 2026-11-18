
/****************************************************************************
 * waterfox                                                           *
 * " SHIMORA "                                                    *
 * version: 160                                                         *
 * url: https://github.com/SHIMORA-6600X/ZenFox
 * licence: MIT
****************************************************************************/

/****************************************************************************
 * SECTION: ZENFOX                                               *
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

/** TRACKING PROTECTION ***/
user_pref("browser.contentblocking.category", "strict");
user_pref("browser.download.start_downloads_in_tmp_dir", true);

 /** TAB UNLOAD ***/                                                      
user_pref("browser.tabs.unloadOnLowMemory", true); // DEFAULT

// 4GB=3276, 8GB=6553, 16GB=13107, 32GB=25698, 64GB=52429
user_pref("browser.low_commit_space_threshold_mb", 3276); // default=200; WINDOWS LINUX
user_pref("browser.tabs.min_inactive_duration_before_unload", 300000);

/** GFX RENDERING TWEAKS ***/                                          
user_pref("gfx.webrender.all", true); // enables WR + additional features
user_pref("gfx.webrender.precache-shaders", true); // longer initial startup time
user_pref("gfx.webrender.compositor", true); // DEFAULT WINDOWS macOS
user_pref("gfx.webrender.compositor.force-enabled", true); // enforce
user_pref("gfx.webrender.layer-compositor", true); // [DEFAULT FF152]
user_pref("media.wmf.zero-copy-nv12-textures-force-enabled", true);
user_pref("gfx.canvas.accelerated", true); // [DEFAULT FF133+]
user_pref("gfx.canvas.accelerated.cache-items", 2048); // [DEFAULT FF135+]
user_pref("gfx.canvas.accelerated.cache-size", 512); // default=256; Chrome=512; max=2048
user_pref("gfx.canvas.max-size", 65535); // [DEFAULT FF152]

/** DISK CACHE ***/
user_pref("browser.cache.disk.smart_size.enabled", false);
user_pref("browser.cache.disk.capacity", 1024000); // default=256000; size of disk cache; 1024000=1GB, 2048000=2GB
user_pref("browser.cache.disk.max_entry_size", 51200); // DEFAULT (50 MB); maximum size of an object in disk cache
user_pref("browser.cache.disk.metadata_memory_limit", 1024); // DEFAULT (1 MB); limit of recent metadata we keep in memory for faster access
user_pref("browser.cache.disk.preload_chunk_count", 8); // default=4
user_pref("browser.cache.frecency_half_life_hours", 6); // DEFAULT
user_pref("browser.cache.disk.max_chunks_memory_usage", 40960); // DEFAULT (40 MB)
user_pref("browser.cache.disk.max_priority_chunks_memory_usage", 40960); // DEFAULT (40 MB)

/** SHUTDOWN & SANITIZING ***/
user_pref("privacy.history.custom", true);
user_pref("browser.privatebrowsing.resetPBM.enabled", true);

/** SPECULATIVE LOADING ***/
user_pref("network.http.speculative-parallel-limit", 0);
user_pref("browser.urlbar.speculativeConnect.enabled", false);
user_pref("browser.places.speculativeConnect.enabled", false);
user_pref("network.prefetch-next", false);

/** HTTPS-ONLY MODE ***/
user_pref("dom.security.https_only_mode", true);
user_pref("dom.security.https_only_mode_error_page_user_suggestions", true);

/** PASSWORDS ***/
user_pref("signon.formlessCapture.enabled", false);
user_pref("signon.privateBrowsingCapture.enabled", false);


/** MEMORY CACHE ***/
user_pref("browser.cache.memory.capacity", 65536); // default=32768 (32 MB)
user_pref("browser.cache.memory.max_entry_size", 10240); // default=5120 (5 MB)
user_pref("browser.sessionhistory.max_total_viewers", -1); // DEFAULT
user_pref("browser.sessionstore.max_tabs_undo", 10); // default=25
user_pref("browser.sessionstore.max_entries", 10); // [HIDDEN OR REMOVED]
user_pref("dom.storage.default_quota", 20480); // 20MB; default=5120
user_pref("dom.storage.shadow_writes", true);

/** NETWORK ***/
user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
user_pref("network.buffer.cache.count", 48); // default=24; 128 too large
user_pref("network.http.max-connections", 1800); // default=900
user_pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive
user_pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
user_pref("network.http.max-persistent-connections-per-proxy", 32); // default=32
user_pref("network.http.request.max-start-delay", 5); // default=10
user_pref("network.websocket.max-connections", 200);
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire
user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]
user_pref("network.ssl_tokens_cache_capacity", 8192);
user_pref("network.dnsCacheEntries", 1600);
user_pref("network.http.pacing.requests.enabled", false);
user_pref("network.http.pacing.requests.min-parallelism", 12); // default=6
user_pref("network.http.pacing.requests.burst", 20);

/****************************************************************************
 * SECTION: LITEFOX                                                     *
****************************************************************************/
/** MOZILLA UI ***/
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.shell.checkDefaultBrowser", false);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.aboutwelcome.enabled", false); // disable Intro screens
user_pref("startup.homepage_welcome_url", "");
user_pref("startup.homepage_welcome_url.additional", "");
user_pref("startup.homepage_override_url", "");

/** THEME ADJUSTMENTS ***/
user_pref("browser.privateWindowSeparation.enabled", false); // WINDOWS
user_pref("layout.css.prefers-color-scheme.content-override", 0);
user_pref("browser.compactmode.show", true);
user_pref("widget.non-native-theme.scrollbar.style", 1);

/** FULLSCREEN NOTICE ***/
user_pref("full-screen-api.transition-duration.enter", "0 0");
user_pref("full-screen-api.transition-duration.leave", "0 0");
user_pref("full-screen-api.warning.timeout", 0);

/** NEW TAB PAGE ***/
user_pref("browser.newtabpage.activity-stream.default.sites", "");
user_pref("browser.newtabpage.activity-stream.showSponsoredTopSites", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
user_pref("browser.newtabpage.activity-stream.showSponsoredCheckboxes", false);

 /** SECTION: NEW TAB PAGE ***/                                                   
 user_pref("browser.startup.page", 1);
 user_pref("browser.startup.homepage", "about:home");
 user_pref("browser.newtabpage.enabled", true);

/** URL BAR ***/                                                        

// PREF: minimize URL bar suggestions (bookmarks, history, open tabs)
// Dropdown options in the URL bar:
user_pref("browser.urlbar.suggest.history", false);
user_pref("browser.urlbar.suggest.bookmark", false); // DEFAULT
user_pref("browser.urlbar.suggest.clipboard", false);
user_pref("browser.urlbar.suggest.openpage",false);
user_pref("browser.urlbar.suggest.engines", true);
user_pref("browser.urlbar.suggest.searches", true);
user_pref("browser.urlbar.quickactions.enabled", false);
user_pref("browser.urlbar.suggest.weather", false); // DEFAULT [FF108]
user_pref("browser.urlbar.weather.ignoreVPN", false); // DEFAULT
user_pref("browser.urlbar.suggest.calculator", false); // [DEFAULT FF137+]
user_pref("browser.urlbar.unitConversion.enabled", false); // [DEFAULT FF141+]
user_pref("browser.urlbar.addons.featureGate", true); // [FF115+]
user_pref("browser.urlbar.amp.featureGate", false); // [FF141+] adMarketplace
user_pref("browser.urlbar.fakespot.featureGate", false); // [FF130+] [DEFAULT: false]
user_pref("browser.urlbar.mdn.featureGate", false); // [FF117+] [HIDDEN PREF]
user_pref("browser.urlbar.weather.featureGate", false); // [FF108+] [DEFAULT: false]
user_pref("browser.urlbar.wikipedia.featureGate", false); // [FF141+]
user_pref("browser.urlbar.clipboard.featureGate", false); // [FF118+] [DEFAULT: true FF125+]
user_pref("browser.urlbar.yelp.featureGate", false);

/****************************************************************************
 * SECTION: SOFTFOX                                                  *
****************************************************************************/
/** SMOOTH SCROLLING ***/
user_pref("apz.overscroll.enabled", true); // DEFAULT NON-LINUX
user_pref("general.smoothScroll", true); // DEFAULT
user_pref("general.smoothScroll.msdPhysics.enabled", true);
user_pref("mousewheel.default.delta_multiplier_y", 320); // 250-400; adjust this number to your liking
