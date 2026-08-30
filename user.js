
/****************************************************************************************
INFORMATION                                   *
 ***************************************************************************************/
// NitroFox                                                                             
// SHIMORA                                                                     
// priority: Fastest browsing                                                          
// version: 152                                                                         
// url: https://github.com/SHIMORA-6600X/NitroFox 
// License : MIT
/****************************************************************************
 * SECTION: GENERAL                                                        *
****************************************************************************/
/
// PREF: initial paint delay
user_pref("nglayout.initialpaint.delay", 5); // DEFAULT; formerly 250
user_pref("nglayout.initialpaint.delay_in_oopif", 5); // DEFAULT

// PREF: Font rendering cache in Skia (32MB)
user_pref("gfx.content.skia-font-cache-size", 20); // 20 MB; default=5; Chrome=20

// PREF: page reflow timer
// true = do not reflow pages at an interval any higher than that specified by content.notify.interval (default)
// false = reflow pages whenever new data is received
user_pref("content.notify.ontimer", true); // DEFAULT

// [EXAMPLE] 100000 = .10s = 100 reflows/second
user_pref("content.notify.interval", 100000); // (.10s); default=120000 (.12s)
user_pref("content.max.tokenizing.time", 1000000); // (1.00s); alt=2000000; HIDDEN
user_pref("content.interrupt.parsing", true); // HIDDEN

// PREF: UI responsiveness threshold
user_pref("content.switch.threshold", 300000); // HIDDEN; default= 750000; alt=500000

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
user_pref("gfx.webrender.layer-compositor", true);

// PREF: improve CPU usage on AMD systems
//user_pref("media.wmf.zero-copy-nv12-textures-force-enabled", true);

// PREF: if your hardware doesn't support Webrender, you can fallback to Webrender's software renderer
//user_pref("gfx.webrender.software", true); // Software Webrender uses CPU instead of GPU
    //user_pref("gfx.webrender.software.opengl", true); // LINUX

// PREF: GPU-accelerated Canvas2D
user_pref("gfx.canvas.accelerated", true); // [DEFAULT FF133+]
user_pref("gfx.canvas.accelerated.cache-items", 8192); // [DEFAULT FF135+]
user_pref("gfx.canvas.accelerated.cache-size", 512); // default=256; Chrome=512; max=2048
user_pref("gfx.canvas.max-size", 32767); // [DEFAULT]

/****************************************************************************
 * SECTION: JAVASCRIPT OPTIONS                                              *
****************************************************************************/

user_pref("javascript.options.baselinejit.threshold", 50); // default=100
user_pref("javascript.options.ion.threshold", 1500); // DEFAULT

// PREF: decrease concurrent JavaScript garbage collection (GC) threads
// Sets the divisor in the formula: GC threads = CPU threads ÷ divisor (min 1).
// A LOWER value = MORE parallel GC threads. A HIGHER value = FEWER threads.
// Example (24-thread CPU):  divisor 1 → 24 threads | 2 → 12 | 4 (default) → 6 | 12 → 2
// Power users with many cores should LOWER this value, not raise it.
// [NOTE] Mozilla's default of 4 is conservative to avoid thread contention on weak hardware.
//user_pref("javascript.options.concurrent_multiprocess_gcs.cpu_divisor", 4); // DEFAULT

/****************************************************************************
 * SECTION: DISK CACHE                                                     *
****************************************************************************/
user_pref("browser.cache.disk.smart_size.enabled", false);
user_pref("browser.cache.disk.capacity", 1024000); // default=256000; size of disk cache; 1024000=1GB, 2048000=2GB
user_pref("browser.cache.disk.max_entry_size", 51200); // DEFAULT (50 MB); maximum size of an object in disk cache
user_pref("browser.cache.disk.metadata_memory_limit", 1024); // DEFAULT (1 MB); limit of recent metadata we keep in memory for faster access
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

user_pref("browser.cache.memory.capacity", 65536); // default=32768 (32 MB)
user_pref("browser.cache.memory.max_entry_size", 10240); // default=5120 (5 MB)
user_pref("browser.sessionhistory.max_total_viewers", 8); // DEFAULT
user_pref("browser.sessionstore.max_tabs_undo", 10); // default=25
user_pref("browser.sessionstore.max_entries", 10); // [HIDDEN OR REMOVED]
user_pref("dom.storage.default_quota", 20480); // 20MB; default=5120
user_pref("dom.storage.shadow_writes", true);
user_pref("javascript.options.mem.high_water_mark", 128); // DEFAULT [HIDDEN OR REMOVED]

/****************************************************************************
 * SECTION: MEDIA CACHE                                                     *
****************************************************************************/

user_pref("media.cache_size", 512000); // DEFAULT
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
user_pref("media.cache_readahead_limit", 3600); // 10 min; default=60; stop reading ahead when our buffered data is this many seconds ahead of the current playback
user_pref("media.cache_resume_threshold", 1800); // 5 min; default=30; when a network connection is suspended, don't resume it until the amount of buffered data falls below this threshold

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

user_pref("network.buffer.cache.size", 65535); // default=32768 (32 kb); 262144 too large
user_pref("network.buffer.cache.count", 48); // default=24; 128 too large
user_pref("network.http.max-connections", 1800); // default=900
user_pref("network.http.max-persistent-connections-per-server", 10); // default=6; download connections; anything above 10 is excessive
user_pref("network.http.max-urgent-start-excessive-connections-per-host", 5); // default=3
user_pref("network.http.max-persistent-connections-per-proxy", 32); // default=32
user_pref("network.http.request.max-start-delay", 5); // default=10
user_pref("network.websocket.max-connections", 200); // DEFAULT

// PREF: pacing requests [FF23+].
// false = Firefox will send as many requests as possible without pacing
// true = Firefox will pace requests (default)
user_pref("network.http.pacing.requests.enabled", false);
user_pref("network.http.pacing.requests.min-parallelism", 12); // default=6
user_pref("network.http.pacing.requests.burst", 20); // default=10
user_pref("network.dnsCacheEntries", 1600); // default=800
user_pref("network.dnsCacheExpiration", 3600); // keep entries for 1 hour; default=60
user_pref("network.dnsCacheExpirationGracePeriod", 120); // default=60; cache DNS entries for 2 minutes after they expire

// PREF: the number of threads for DNS
user_pref("network.dns.max_high_priority_threads", 40); // DEFAULT [FF 123?]
user_pref("network.dns.max_any_priority_threads", 24); // DEFAULT [FF 123?]

// PREF: increase TLS token caching 
user_pref("network.ssl_tokens_cache_capacity", 8192); // TLS token caching (fast reconnects)

/****************************************************************************
 * SECTION: TAB UNLOAD                                                      *
****************************************************************************/

// PREF: unload tabs on low memory
user_pref("browser.tabs.unloadOnLowMemory", true); // DEFAULT

// PREF: determine when tabs unload [WINDOWS] [LINUX]
// Notify TabUnloader or send the memory pressure if the memory resource
// notification is signaled AND the available commit space is lower than
// this value (in MiB).
// Set this to some value, e.g. 4/5 of total memory available on your system:
// 4GB=3276, 8GB=6553, 16GB=13107, 32GB=25698, 64GB=52429
user_pref("browser.low_commit_space_threshold_mb", 3276); // default=200; WINDOWS LINUX

// PREF: determine how long (in ms) tabs are inactive before they unload
// 60000=1min; 300000=5min; 600000=10min (default)
user_pref("browser.tabs.min_inactive_duration_before_unload", 300000); // 5min; default=600000
