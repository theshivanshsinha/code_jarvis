import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import SimpleCalendar from "../components/SimpleCalendar";

export default function Home() {
  const navigate = useNavigate();
  const token = useMemo(() => localStorage.getItem("session_token"), []);

  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [hoverPlatform, setHoverPlatform] = useState(null); // 'leetcode'|'codeforces'|'atcoder'|'codechef'|null
  const [hoverTimeout, setHoverTimeout] = useState(null);
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [platformDetails, setPlatformDetails] = useState(null);
  const [loadingPlatformDetails, setLoadingPlatformDetails] = useState(false);
  const [loadingStats, setLoadingStats] = useState(true);
  const [contests, setContests] = useState([]);
  const [loadingContests, setLoadingContests] = useState(true);
  const [message, setMessage] = useState("");
  const [daily, setDaily] = useState([]);
  const [problemHistory, setProblemHistory] = useState([]);
  const [loadingProblems, setLoadingProblems] = useState(false);
  const [showProblemHistory, setShowProblemHistory] = useState(false);
  const [platformFilter, setPlatformFilter] = useState("all");
  const [searchFilter, setSearchFilter] = useState("");
  const [next7Only, setNext7Only] = useState(false);
  const [contestReminders, setContestReminders] = useState(new Set()); // Track which contests have reminders
  const [activeTab, setActiveTab] = useState("dashboard"); // New tab state

  // Tab rendering functions
  const renderTabContent = () => {
    switch (activeTab) {
      case "dashboard":
        return renderDashboardTab();
      case "problems":
        return <TopProblems />;
      case "dsa-rush":
        return <DSACodeRush />;
      case "contests":
        return renderContestsTab();
      case "codespace":
        return <CodeSpaceTab />;
      default:
        return renderDashboardTab();
    }
  };

  const renderDashboardTab = () => (
    <>
      <div className="mt-6 grid md:grid-cols-3 gap-6">
        {loadingStats ? (
          <div className="md:col-span-2">
            <div className="bg-gray-800/60 border border-gray-700 rounded p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="h-6 bg-gray-700 rounded w-32 animate-pulse"></div>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="bg-gray-800 border border-gray-700 rounded p-3"
                  >
                    <div className="h-4 bg-gray-700 rounded w-20 animate-pulse mb-2"></div>
                    <div className="h-6 bg-gray-700 rounded w-16 animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>
            <div className="mt-4 bg-gray-800/60 border border-gray-700 rounded p-4">
              <div className="h-6 bg-gray-700 rounded w-40 animate-pulse mb-4"></div>
              <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className="bg-gray-800/60 border border-gray-700 rounded-lg p-4 text-center"
                  >
                    <div className="mx-auto w-12 h-12 rounded-full bg-gray-700 animate-pulse mb-3"></div>
                    <div className="h-4 bg-gray-700 rounded w-16 mx-auto animate-pulse mb-2"></div>
                    <div className="h-3 bg-gray-700 rounded w-12 mx-auto animate-pulse"></div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : stats ? (
          <div className="md:col-span-2">
            <div className="bg-gray-800/60 border border-gray-700 rounded p-4">
              <div className="flex items-center justify-between mb-2">
                <div className="text-xl font-semibold">Overview</div>
                {Array.isArray(stats.overview?.topics || stats.topics) &&
                  (stats.overview?.topics || stats.topics).length > 0 && (
                    <div className="hidden md:flex flex-wrap gap-2 text-xs">
                      {(stats.overview?.topics || stats.topics)
                        .slice(0, 6)
                        .map((t, i) => (
                          <TopicBadge key={i} name={t.name} level={t.level} />
                        ))}
                    </div>
                  )}
              </div>
              {hoverPlatform && stats?.perPlatform?.[hoverPlatform] ? (
                <div className="grid sm:grid-cols-3 gap-4 text-sm text-gray-300">
                  <OverviewStatCard
                    label="Total Solved"
                    value={stats.perPlatform[hoverPlatform].totalSolved}
                  />
                  <OverviewStatCard
                    label="Easy / Med / Hard"
                    value={`${stats.perPlatform[hoverPlatform].easy} / ${stats.perPlatform[hoverPlatform].medium} / ${stats.perPlatform[hoverPlatform].hard}`}
                  />
                  <OverviewStatCard
                    label="Rank/Rating"
                    value={stats.perPlatform[hoverPlatform].rank}
                  />
                  <OverviewStatCard
                    label="Streak"
                    value={`${stats.perPlatform[hoverPlatform].streak} days`}
                  />
                  <OverviewStatCard
                    label="Contests"
                    value={stats.perPlatform[hoverPlatform].contestCount}
                  />
                </div>
              ) : (
                <div className="grid sm:grid-cols-3 gap-4 text-sm text-gray-300">
                  <OverviewStatCard
                    label="Total Contests"
                    value={stats.overview?.totalContests}
                  />
                  <OverviewStatCard
                    label="Max Rating"
                    value={`${stats.overview?.maxRating?.platform || ""} ${
                      stats.overview?.maxRating?.value || ""
                    }`}
                  />
                  <OverviewStatCard
                    label="Solved"
                    value={`LC ${
                      stats.overview?.problemsSolved?.leetcode || 0
                    }, CF ${stats.overview?.problemsSolved?.codeforces || 0}`}
                  />
                </div>
              )}
              {Array.isArray(stats.overview?.topics || stats.topics) &&
                (stats.overview?.topics || stats.topics).length > 0 && (
                  <div className="mt-3 md:hidden flex flex-wrap gap-2">
                    {(stats.overview?.topics || stats.topics)
                      .slice(0, 6)
                      .map((t, i) => (
                        <TopicBadge key={i} name={t.name} level={t.level} />
                      ))}
                  </div>
                )}
            </div>
            <div className="mt-4 bg-gray-800/60 border border-gray-700 rounded p-4">
              <LinkedAccounts
                accounts={accounts}
                stats={stats}
                onHover={handlePlatformHover}
                onLeave={handlePlatformLeave}
                onPlatformClick={handlePlatformClick}
              />
            </div>
          </div>
        ) : (
          <div className="md:col-span-2">
            <div className="bg-gray-800/60 border border-gray-700 rounded p-4 text-center py-8">
              <div className="text-gray-400 mb-2">
                Unable to load statistics
              </div>
              <div className="text-sm text-gray-500">
                Please check your connection and try again
              </div>
            </div>
          </div>
        )}
        <div className="bg-gray-800/60 border border-gray-700 rounded p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="text-xl font-semibold">Daily activity</div>
            <div className="flex gap-2">
              <button
                onClick={fetchProblemHistory}
                disabled={loadingProblems}
                className="px-4 py-2 text-sm rounded-lg bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-blue-500/25"
                title="View recent problem submissions"
              >
                {loadingProblems ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Loading
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    Problem History
                  </div>
                )}
              </button>
            </div>
          </div>
          <Heatmap days={daily} />
        </div>
      </div>

      {/* Contest Calendar Section */}
      <div className="mt-6">
        <SimpleCalendar
          userEmail={user?.email || localStorage.getItem("userEmail")}
        />
      </div>
    </>
  );

  const renderContestsTab = () => (
    <div className="grid md:grid-cols-3 gap-6">
      <div className="md:col-span-3 bg-gray-800/60 border border-gray-700 rounded p-4">
        <div className="flex items-center justify-between mb-3 gap-2">
          <div className="text-lg font-semibold">Upcoming Contests</div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setNext7Only((v) => !v)}
              className={`px-2 py-1 rounded border text-sm ${
                next7Only
                  ? "bg-emerald-900 border-emerald-800 text-emerald-300"
                  : "bg-gray-900 border-gray-700"
              }`}
              title="Show contests in the next 7 days"
            >
              Next 7 days
            </button>
            <select
              value={platformFilter}
              onChange={(e) => setPlatformFilter(e.target.value)}
              className="px-2 py-1 rounded bg-gray-900 border border-gray-700 text-sm"
              title="Filter by platform"
            >
              <option value="all">All platforms</option>
              <option value="Codeforces">Codeforces</option>
              <option value="LeetCode">LeetCode</option>
              <option value="AtCoder">AtCoder</option>
              <option value="CodeChef">CodeChef</option>
            </select>
            <input
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search contests"
              className="px-2 py-1 rounded bg-gray-900 border border-gray-700 text-sm"
              title="Search by contest name"
            />
            <a
              href="/dashboard"
              className="text-sm text-blue-300 hover:text-blue-200"
            >
              Open full view
            </a>
          </div>
        </div>
        <CalendarStrip
          contests={contests}
          next7Only={next7Only}
          platformFilter={platformFilter}
          searchFilter={searchFilter}
        />
        {loadingContests ? (
          <div>Loading…</div>
        ) : (
          <div className="grid sm:grid-cols-2 gap-4">
            {contests
              .filter(
                (c) =>
                  platformFilter === "all" || c.platform === platformFilter
              )
              .filter((c) =>
                c.name.toLowerCase().includes(searchFilter.toLowerCase())
              )
              .filter((c) => {
                if (!next7Only) return true;
                const now = new Date();
                const in7 = new Date();
                in7.setDate(in7.getDate() + 7);
                const cs = new Date(c.start);
                return cs >= now && cs <= in7;
              })
              .map((c, idx) => (
                <div
                  key={idx}
                  className="bg-gray-800 border border-gray-700 rounded p-4"
                  title={`${c.platform} • ${new Date(
                    c.start
                  ).toLocaleString()} • ${c.durationMinutes} min`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-blue-300">
                      {c.platform}
                    </span>
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-gray-900 border border-gray-700">
                      {Math.round(c.durationMinutes / 60)}h
                    </span>
                  </div>
                  <div className="text-lg font-semibold mt-0.5">
                    {c.name}
                  </div>
                  <div className="text-sm text-gray-300 mt-1">
                    Starts: {new Date(c.start).toLocaleString()}
                  </div>
                  <div className="text-sm text-gray-300">
                    Duration: {c.durationMinutes} min
                  </div>
                  <div className="mt-3 flex gap-3">
                    <a
                      href={c.url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1 rounded bg-blue-600 hover:bg-blue-500"
                      title="Open registration page"
                    >
                      Register
                    </a>
                    <button
                      onClick={() => remind(c)}
                      className={`px-3 py-1 rounded transition-colors ${
                        contestReminders.has(
                          `${c.platform}:${c.name}:${c.url}`
                        )
                          ? "bg-red-600 hover:bg-red-500"
                          : "bg-gray-700 hover:bg-gray-600"
                      }`}
                      title={
                        contestReminders.has(
                          `${c.platform}:${c.name}:${c.url}`
                        )
                          ? "Remove reminder"
                          : "Create a reminder"
                      }
                    >
                      {contestReminders.has(
                        `${c.platform}:${c.name}:${c.url}`
                      )
                        ? "Unremind"
                        : "Remind me"}
                    </button>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );

  const [accounts, setAccounts] = useState({
    codeforces: "",
    leetcode: "",
    atcoder: "",
    codechef: "",
  });
  const [savingAccounts, setSavingAccounts] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [prefs, setPrefs] = useState({
    emailReminders: true,
    newsletter: false,
    avatar: "",
  });

  useEffect(() => {
    if (!token) {
      navigate("/", { replace: true });
      return;
    }
    fetch("http://localhost:5000/api/auth/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setUser(data.user || null))
      .catch(() => setUser(null));

    setLoadingStats(true);
    fetch("http://localhost:5000/api/stats", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then(setStats)
      .catch(() => setStats(null))
      .finally(() => setLoadingStats(false));

    fetch("http://localhost:5000/api/stats/daily", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => r.json())
      .then((data) => setDaily(data.days || []))
      .catch(() => setDaily([]));

    fetch("http://localhost:5000/api/contests")
      .then((r) => r.json())
      .then((data) => setContests(data))
      .finally(() => setLoadingContests(false));

    fetch("http://localhost:5000/api/accounts", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => (r.ok ? r.json() : { accounts: {} }))
      .then((data) =>
        setAccounts((prev) => ({ ...prev, ...(data.accounts || {}) }))
      )
      .catch(() => {});

    const savedAvatar = localStorage.getItem("profile_avatar") || "";
    if (savedAvatar) {
      setPrefs((p) => ({ ...p, avatar: savedAvatar }));
    }
  }, [navigate, token]);

  const checkExistingReminders = async () => {
    try {
      const userEmail = user?.email || localStorage.getItem("userEmail");
      if (!userEmail) return;

      const response = await fetch(
        `http://localhost:5000/api/reminders/${encodeURIComponent(userEmail)}`
      );
      const data = await response.json();

      if (data.success && data.reminders) {
        const reminderSet = new Set();
        data.reminders.forEach((reminder) => {
          // Extract platform and contest name from contest_name (format: "Platform: Contest Name")
          const parts = reminder.contest_name.split(": ");
          if (parts.length >= 2) {
            const platform = parts[0];
            const contestName = parts.slice(1).join(": ");
            const key = `${platform}:${contestName}:${reminder.contest_url}`;
            reminderSet.add(key);
          }
        });
        setContestReminders(reminderSet);
      }
    } catch (error) {
      console.error("Failed to check existing reminders:", error);
    }
  };

  // Update daily activity when hovering a platform
  useEffect(() => {
    const endpoint = hoverPlatform
      ? `http://localhost:5000/api/stats/daily?platform=${encodeURIComponent(
          hoverPlatform
        )}`
      : `http://localhost:5000/api/stats/daily`;
    fetch(endpoint, { headers: { Authorization: `Bearer ${token}` } })
      .then((r) => r.json())
      .then((data) => setDaily(data.days || []))
      .catch(() => {});
  }, [hoverPlatform, token]);

  // Check existing reminders when user or contests change
  useEffect(() => {
    if (user && contests.length > 0) {
      checkExistingReminders();
    }
  }, [user, contests]);

  const remind = async (contest) => {
    try {
      const userEmail = user?.email || localStorage.getItem("userEmail");
      if (!userEmail) {
        setMessage("Please sign in to set reminders");
        setTimeout(() => setMessage(""), 3000);
        return;
      }

      const contestKey = `${contest.platform}:${contest.name}:${contest.url}`;

      // Check if reminder already exists
      if (contestReminders.has(contestKey)) {
        // Remove reminder
        const res = await fetch("http://localhost:5000/api/reminders", {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_email: userEmail,
            contest_name: `${contest.platform}: ${contest.name}`,
            contest_url: contest.url,
          }),
        });

        const data = await res.json();

        if (res.ok && data.success) {
          setContestReminders((prev) => {
            const newSet = new Set(prev);
            newSet.delete(contestKey);
            return newSet;
          });
          setMessage("Reminder removed successfully!");
        } else {
          setMessage(data.error || "Failed to remove reminder");
        }
      } else {
        // Create reminder
        const res = await fetch("http://localhost:5000/api/reminders", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            user_email: userEmail,
            contest_name: `${contest.platform}: ${contest.name}`,
            contest_url: contest.url,
            contest_time: contest.start,
            platform: contest.platform,
          }),
        });

        const data = await res.json();

        if (res.ok && data.success) {
          setContestReminders((prev) => new Set(prev).add(contestKey));
          setMessage("Reminder created successfully! Check your email.");
        } else {
          if (res.status === 409) {
            setContestReminders((prev) => new Set(prev).add(contestKey));
            setMessage("Reminder already exists for this contest");
          } else {
            setMessage(data.error || "Failed to create reminder");
          }
        }
      }

      setTimeout(() => setMessage(""), 3000);
    } catch (e) {
      console.error("Reminder error:", e);
      setMessage(e.message || "Failed to manage reminder");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  const saveAccounts = async () => {
    try {
      setSavingAccounts(true);
      const res = await fetch("http://localhost:5000/api/accounts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ accounts }),
      });
      if (!res.ok) throw new Error("Failed");
      setMessage("Accounts linked");
      setTimeout(() => setMessage(""), 2000);
    } catch (e) {
      setMessage("Failed to save accounts");
      setTimeout(() => setMessage(""), 2000);
    } finally {
      setSavingAccounts(false);
    }
  };

  const handlePlatformClick = async (platform) => {
    setSelectedPlatform(platform);
    setLoadingPlatformDetails(true);
    setPlatformDetails(null);

    try {
      const response = await fetch(
        `http://localhost:5000/api/stats/${platform}?detailed=true`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const data = await response.json();
      setPlatformDetails(data);
    } catch (error) {
      console.error("Failed to fetch platform details:", error);
      setMessage("Failed to load platform details");
      setTimeout(() => setMessage(""), 3000);
    } finally {
      setLoadingPlatformDetails(false);
    }
  };

  const closePlatformModal = () => {
    setSelectedPlatform(null);
    setPlatformDetails(null);
  };

  const fetchProblemHistory = async () => {
    console.log("🔍 Fetching problem history...");
    console.log("Token available:", !!token);
    console.log("Connected accounts:", accounts);
    console.log("User state:", user);

    setLoadingProblems(true);
    try {
      // Always try to get data - the backend handles demo data automatically
      let url = `http://localhost:5000/api/stats/problems?limit=50&days=90`;
      let headers = {
        "Content-Type": "application/json",
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
        console.log("Making authenticated request with token");
      } else {
        console.log("Making unauthenticated request (will get demo data)");
      }

      console.log("Request URL:", url);
      console.log("Request headers:", headers);

      const response = await fetch(url, {
        method: "GET",
        headers: headers,
      });

      console.log("Response status:", response.status);
      console.log(
        "Response headers:",
        Object.fromEntries(response.headers.entries())
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Response error body:", errorText);
        throw new Error(
          `HTTP ${response.status}: ${response.statusText} - ${errorText}`
        );
      }

      const data = await response.json();
      console.log("Full response data:", JSON.stringify(data, null, 2));
      console.log("Problems array:", data.problems);
      console.log("Problems count:", data.problems?.length || 0);
      console.log("Response total:", data.total);
      console.log("Response filters:", data.filters);

      // Always show the modal first
      setShowProblemHistory(true);

      if (
        data.problems &&
        Array.isArray(data.problems) &&
        data.problems.length > 0
      ) {
        setProblemHistory(data.problems);
        console.log(
          "✅ Successfully set problem history with",
          data.problems.length,
          "problems"
        );
        setMessage(`Loaded ${data.problems.length} recent problems`);
        setTimeout(() => setMessage(""), 3000);
      } else {
        setProblemHistory([]);
        console.log("⚠️ No problems returned from API");
        console.log("Available data keys:", Object.keys(data));

        // Check if it's because user has no connected accounts
        if (
          token &&
          Object.values(accounts).every((acc) => !acc || acc.length === 0)
        ) {
          console.log("User is authenticated but has no connected accounts");
          setMessage(
            "Connect your coding accounts in Settings to see your problem history"
          );
        } else if (token) {
          console.log("User has connected accounts but no problems found");
          setMessage(
            "No recent problems found. Try solving some problems and refresh!"
          );
        } else {
          console.log("No authentication token - should show demo data");
          setMessage("Demo data not available. Please try again.");
        }
        setTimeout(() => setMessage(""), 5000);
      }
    } catch (error) {
      console.error("❌ Failed to fetch problem history:", error);
      setProblemHistory([]);
      setMessage(`Failed to load problem history: ${error.message}`);
      setTimeout(() => setMessage(""), 5000);
      setShowProblemHistory(true); // Still show the modal so user sees the error
    } finally {
      setLoadingProblems(false);
    }
  };

  // Smooth hover handlers with debouncing
  const handlePlatformHover = (platform) => {
    // Clear any existing timeout
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
    }

    // Set new hover platform immediately for smooth visual feedback
    setHoverPlatform(platform);
  };

  const handlePlatformLeave = () => {
    // Add a small delay before clearing hover to prevent flicker
    const timeout = setTimeout(() => {
      setHoverPlatform(null);
    }, 150); // 150ms delay

    setHoverTimeout(timeout);
  };

  // Clean up timeout on unmount
  useEffect(() => {
    return () => {
      if (hoverTimeout) {
        clearTimeout(hoverTimeout);
      }
    };
  }, [hoverTimeout]);

  const logout = () => {
    localStorage.removeItem("session_token");
    navigate("/", { replace: true });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white">
      {/* Animated background elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-600/10 rounded-full blur-3xl animate-pulse"></div>
        <div
          className="absolute -bottom-40 -left-40 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "1s" }}
        ></div>
        <div
          className="absolute top-1/3 left-1/4 w-64 h-64 bg-emerald-600/5 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "2s" }}
        ></div>
      </div>

      <div className="relative max-w-7xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-12 h-12 bg-gradient-to-br from-emerald-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-2xl border border-white/20">
                <svg
                  className="w-7 h-7 text-white drop-shadow-lg"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2.5}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full animate-ping"></div>
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full"></div>
            </div>
            <div>
              <div className="flex items-center gap-3">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-white via-purple-200 to-cyan-200 bg-clip-text text-transparent">
                  CodeJarvis
                </h1>
                <span className="px-2 py-1 bg-gradient-to-r from-emerald-500/20 to-cyan-500/20 border border-emerald-500/30 rounded-lg text-emerald-400 text-xs font-semibold">
                  v1.0
                </span>
              </div>
              <p className="text-sm text-gray-400 font-medium">
                Your AI-powered competitive programming companion
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-sm text-gray-300">
            <button
              onClick={() => setShowSettings(true)}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-gray-800/80 to-gray-700/80 hover:from-gray-700/80 hover:to-gray-600/80 border border-gray-600/50 hover:border-gray-500/50 flex items-center gap-2 transition-all duration-200 backdrop-blur-sm shadow-lg hover:shadow-xl"
              title="Open settings"
            >
              <svg
                className="w-4 h-4 text-gray-300"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09a1.65 1.65 0 0 0-1-1.51 1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09a1.65 1.65 0 0 0 1.51-1 1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9c0 .66.26 1.3.73 1.77.47.47 1.11.73 1.77.73H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
              </svg>
              Settings
            </button>
            {user && (
              <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-gradient-to-r from-gray-800/60 to-gray-700/60 border border-gray-600/50 backdrop-blur-sm">
                {prefs.avatar ? (
                  <img
                    src={prefs.avatar}
                    alt="avatar"
                    className="w-8 h-8 rounded-xl object-cover border-2 border-purple-500/30 shadow-lg"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-500 to-blue-500 border-2 border-white/20 flex items-center justify-center text-white text-sm font-bold shadow-lg">
                    {(user.name || user.email || "").slice(0, 1).toUpperCase()}
                  </div>
                )}
                <div className="flex flex-col">
                  <span className="text-white font-medium text-sm leading-tight">
                    {user.name || user.email}
                  </span>
                  <span className="text-gray-400 text-xs leading-tight">
                    Active User
                  </span>
                </div>
              </div>
            )}
            <button
              onClick={logout}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-red-600/80 to-red-500/80 hover:from-red-500/80 hover:to-red-400/80 border border-red-500/50 hover:border-red-400/50 text-white font-medium transition-all duration-200 flex items-center gap-2 shadow-lg hover:shadow-red-500/25"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              Logout
            </button>
          </div>
        </div>

        {message && (
          <div className="mb-6 p-4 rounded-2xl border bg-gradient-to-r from-emerald-500/10 to-cyan-500/10 border-emerald-500/30 flex items-center gap-3 backdrop-blur-sm">
            <div className="w-8 h-8 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-xl flex items-center justify-center">
              <svg
                className="w-5 h-5 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <div className="flex-1">
              <div className="text-emerald-400 font-medium">{message}</div>
            </div>
            <button
              onClick={() => setMessage("")}
              className="p-1 rounded-lg hover:bg-white/10 text-emerald-400 hover:text-white transition-colors"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="mb-8 bg-gray-800/60 border border-gray-700 rounded-2xl p-2">
          <nav className="flex items-center gap-2">
            {[
              { id: "dashboard", label: "Dashboard", icon: "📊" },
              { id: "problems", label: "Top Problems", icon: "🎯" },
              { id: "dsa-rush", label: "DSA CodeRush", icon: "🚀" },
              { id: "contests", label: "Contests", icon: "🏆" },
              { id: "codespace", label: "CodeSpace", icon: "💻" }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 rounded-xl font-medium transition-all duration-200 ${
                  activeTab === tab.id
                    ? "bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg shadow-blue-500/25"
                    : "text-gray-300 hover:bg-gray-700/50 hover:text-white"
                }`}
              >
                <span className="text-lg">{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {renderTabContent()}
      </div>
      {showSettings && (
        <SettingsPanel
          onClose={() => setShowSettings(false)}
          accounts={accounts}
          setAccounts={setAccounts}
          prefs={prefs}
          setPrefs={setPrefs}
          onSave={saveAccounts}
          saving={savingAccounts}
          onSaveProfile={() => {
            if (prefs.avatar) {
              localStorage.setItem("profile_avatar", prefs.avatar);
              setMessage("Profile updated");
              setTimeout(() => setMessage(""), 1500);
            }
          }}
        />
      )}

      {showProblemHistory && (
        <ProblemHistoryModal
          problems={problemHistory}
          onClose={() => setShowProblemHistory(false)}
        />
      )}

      {selectedPlatform && (
        <PlatformModal
          platform={selectedPlatform}
          details={platformDetails}
          loading={loadingPlatformDetails}
          onClose={closePlatformModal}
        />
      )}
    </div>
  );
}

function PlatformModal({ platform, details, loading, onClose }) {
  if (!platform) return null;

  const platformColors = {
    leetcode: "#FFA116",
    codeforces: "#1F8ACB",
    atcoder: "#3F7FBF",
    codechef: "#5B4638",
  };

  const color = platformColors[platform] || "#6B7280";

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="absolute inset-0 bg-black/70" onClick={onClose} />
      <div className="relative min-h-full flex items-center justify-center p-4">
        <div className="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div
            className="px-6 py-4 border-b border-gray-700"
            style={{ backgroundColor: `${color}10` }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-full border-2 flex items-center justify-center"
                  style={{
                    backgroundColor: `${color}20`,
                    borderColor: color,
                    color,
                  }}
                >
                  <PlatformIcon platform={platform} />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white capitalize">
                    {platform} Statistics
                  </h2>
                  {details && (
                    <p className="text-sm text-gray-400">
                      {details.connected
                        ? `@${details.username}`
                        : "Account not connected"}
                    </p>
                  )}
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-gray-800 text-gray-400 hover:text-white transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-80px)]">
            {loading ? (
              <div className="p-8 text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mb-4"></div>
                <p className="text-gray-400">Loading detailed statistics...</p>
              </div>
            ) : details ? (
              <PlatformDetails
                details={details}
                color={color}
                platform={platform}
              />
            ) : (
              <div className="p-8 text-center">
                <p className="text-gray-400">Failed to load platform details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function ProblemHistoryModal({ problems, onClose }) {
  console.log("ProblemHistoryModal rendered with problems:", problems);

  // Check if this looks like demo data
  const isDemoData =
    problems && problems.length > 0 && !localStorage.getItem("session_token");

  // Filter states
  const [filters, setFilters] = useState({
    platform: "all",
    difficulty: "all",
    verdict: "all",
    tags: "",
    sort: "date",
    order: "desc",
    days: 90,
  });

  const [filteredProblems, setFilteredProblems] = useState(problems || []);
  const [loading, setLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);

  // Initialize filtered problems when problems prop changes
  useEffect(() => {
    setFilteredProblems(problems || []);
  }, [problems]);

  // Function to apply filters and fetch filtered data
  const handleFilterChange = async (newFilters) => {
    setLoading(true);
    try {
      const token = localStorage.getItem("session_token");
      const params = new URLSearchParams({
        platform: newFilters.platform,
        difficulty: newFilters.difficulty,
        verdict: newFilters.verdict,
        tags: newFilters.tags,
        sort: newFilters.sort,
        order: newFilters.order,
        days: newFilters.days.toString(),
        limit: "200", // Get more problems for better filtering
      });

      let headers = {
        "Content-Type": "application/json",
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      const response = await fetch(
        `http://localhost:5000/api/stats/problems?${params}`,
        {
          headers,
        }
      );

      if (response.ok) {
        const data = await response.json();
        setFilteredProblems(data.problems || []);
      } else {
        console.error("Failed to fetch filtered problems");
      }
    } catch (error) {
      console.error("Error fetching filtered problems:", error);
    } finally {
      setLoading(false);
    }
  };

  // Handle individual filter changes
  const updateFilter = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    handleFilterChange(newFilters);
  };

  // Reset all filters
  const resetFilters = () => {
    const defaultFilters = {
      platform: "all",
      difficulty: "all",
      verdict: "all",
      tags: "",
      sort: "date",
      order: "desc",
      days: 90,
    };
    setFilters(defaultFilters);
    handleFilterChange(defaultFilters);
  };

  // Check if any filters are active
  const hasActiveFilters = () => {
    return (
      filters.platform !== "all" ||
      filters.difficulty !== "all" ||
      filters.verdict !== "all" ||
      filters.tags !== "" ||
      filters.sort !== "date" ||
      filters.order !== "desc" ||
      filters.days !== 90
    );
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "Unknown";
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  };

  const getVerdictColor = (verdict) => {
    const v = verdict?.toString().toUpperCase();
    if (v === "OK" || v === "AC" || v === "ACCEPTED") {
      return "bg-green-900 text-green-300 border-green-800";
    } else if (v === "WA" || v === "WRONG ANSWER") {
      return "bg-red-900 text-red-300 border-red-800";
    } else if (v === "TLE" || v === "TIME LIMIT EXCEEDED") {
      return "bg-yellow-900 text-yellow-300 border-yellow-800";
    } else {
      return "bg-gray-900 text-gray-300 border-gray-700";
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "text-green-400";
      case "medium":
        return "text-yellow-400";
      case "hard":
        return "text-red-400";
      default:
        return "text-gray-400";
    }
  };

  const getPlatformColor = (platform) => {
    const colors = {
      leetcode: "#FFA116",
      codeforces: "#1F8ACB",
      atcoder: "#3F7FBF",
      codechef: "#5B4638",
    };
    return colors[platform] || "#6B7280";
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="absolute inset-0 bg-black/70" onClick={onClose} />
      <div className="relative min-h-full flex items-center justify-center p-4">
        <div className="relative bg-gray-900 border border-gray-700 rounded-xl shadow-2xl w-full max-w-6xl max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="px-6 py-4 border-b border-gray-700 bg-gray-800">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-4">
                  <div>
                    <h2 className="text-xl font-bold text-white">
                      Problem History {isDemoData && "(Demo Data)"}
                    </h2>
                    <p className="text-sm text-gray-400">
                      {isDemoData
                        ? "Showing sample data from active competitive programmers"
                        : "Recent submissions from all connected platforms"}
                    </p>
                  </div>

                  {/* Filter Toggle Button */}
                  <button
                    onClick={() => setShowFilters(!showFilters)}
                    className={`px-3 py-2 rounded-lg border transition-colors flex items-center gap-2 ${
                      showFilters
                        ? "bg-blue-600 border-blue-500 text-white"
                        : "bg-gray-700 border-gray-600 text-gray-300 hover:bg-gray-600"
                    }`}
                  >
                    <svg
                      className="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"
                      />
                    </svg>
                    Filters
                    {hasActiveFilters() && (
                      <span className="bg-red-500 text-white text-xs rounded-full w-2 h-2"></span>
                    )}
                  </button>

                  {/* Results Count */}
                  <div className="text-sm text-gray-400">
                    {loading ? (
                      <span className="flex items-center gap-2">
                        <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                        Loading...
                      </span>
                    ) : (
                      `${filteredProblems.length} problems`
                    )}
                  </div>
                </div>
              </div>

              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-gray-700 text-gray-400 hover:text-white transition-colors"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            {/* Filter Controls */}
            {showFilters && (
              <div className="mt-4 p-4 bg-gray-700/50 rounded-lg border border-gray-600">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {/* Platform Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Platform
                    </label>
                    <select
                      value={filters.platform}
                      onChange={(e) => updateFilter("platform", e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="all">All Platforms</option>
                      <option value="codeforces">Codeforces</option>
                      <option value="leetcode">LeetCode</option>
                      <option value="atcoder">AtCoder</option>
                    </select>
                  </div>

                  {/* Difficulty Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Difficulty
                    </label>
                    <select
                      value={filters.difficulty}
                      onChange={(e) =>
                        updateFilter("difficulty", e.target.value)
                      }
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="all">All Difficulties</option>
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>

                  {/* Verdict Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Verdict
                    </label>
                    <select
                      value={filters.verdict}
                      onChange={(e) => updateFilter("verdict", e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="all">All Verdicts</option>
                      <option value="AC">Accepted</option>
                      <option value="WA">Wrong Answer</option>
                      <option value="TLE">Time Limit Exceeded</option>
                      <option value="MLE">Memory Limit Exceeded</option>
                      <option value="RE">Runtime Error</option>
                    </select>
                  </div>

                  {/* Days Filter */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Time Period
                    </label>
                    <select
                      value={filters.days}
                      onChange={(e) =>
                        updateFilter("days", parseInt(e.target.value))
                      }
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value={7}>Last 7 days</option>
                      <option value={30}>Last 30 days</option>
                      <option value={90}>Last 90 days</option>
                      <option value={180}>Last 6 months</option>
                      <option value={365}>Last year</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                  {/* Tags Filter */}
                  <div className="md:col-span-1">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Tags (comma-separated)
                    </label>
                    <input
                      type="text"
                      value={filters.tags}
                      onChange={(e) => updateFilter("tags", e.target.value)}
                      placeholder="e.g., dp, graphs, greedy"
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  {/* Sort By */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Sort By
                    </label>
                    <select
                      value={filters.sort}
                      onChange={(e) => updateFilter("sort", e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="date">Date</option>
                      <option value="difficulty">Difficulty</option>
                      <option value="platform">Platform</option>
                    </select>
                  </div>

                  {/* Sort Order */}
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Order
                    </label>
                    <select
                      value={filters.order}
                      onChange={(e) => updateFilter("order", e.target.value)}
                      className="w-full bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="desc">Descending</option>
                      <option value="asc">Ascending</option>
                    </select>
                  </div>
                </div>

                {/* Filter Actions */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-600">
                  <div className="text-sm text-gray-400">
                    {hasActiveFilters()
                      ? "Filters applied"
                      : "No filters applied"}
                  </div>
                  <div className="flex gap-2">
                    {hasActiveFilters() && (
                      <button
                        onClick={resetFilters}
                        className="px-3 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded-lg transition-colors text-sm"
                      >
                        Reset Filters
                      </button>
                    )}
                    <button
                      onClick={() => setShowFilters(false)}
                      className="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors text-sm"
                    >
                      Hide Filters
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6">
            {!filteredProblems || filteredProblems.length === 0 ? (
              <div className="text-center py-12">
                {loading ? (
                  <div className="flex flex-col items-center">
                    <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                    <div className="text-gray-400">
                      Loading filtered problems...
                    </div>
                  </div>
                ) : hasActiveFilters() ? (
                  <div>
                    <div className="text-6xl mb-4">🔍</div>
                    <div className="text-gray-400 mb-2">
                      No problems match your filters
                    </div>
                    <div className="text-sm text-gray-500 mb-6">
                      Try adjusting your filter criteria or reset filters to see
                      all problems.
                    </div>
                    <button
                      onClick={resetFilters}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
                    >
                      Reset Filters
                    </button>
                  </div>
                ) : (
                  <div>
                    <div className="text-6xl mb-4">📚</div>
                    <div className="text-gray-400 mb-2">
                      No problem history available
                    </div>
                    <div className="text-sm text-gray-500 mb-6 max-w-md mx-auto">
                      To see your coding activity here, connect your accounts in
                      Settings and start solving problems on:
                    </div>
                    <div className="flex justify-center gap-6 mb-6">
                      <div className="text-center">
                        <div className="w-12 h-12 bg-orange-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-orange-400 text-lg">LC</span>
                        </div>
                        <div className="text-xs text-gray-400">LeetCode</div>
                      </div>
                      <div className="text-center">
                        <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-blue-400 text-lg">CF</span>
                        </div>
                        <div className="text-xs text-gray-400">Codeforces</div>
                      </div>
                      <div className="text-center">
                        <div className="w-12 h-12 bg-cyan-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                          <span className="text-cyan-400 text-lg">AC</span>
                        </div>
                        <div className="text-xs text-gray-400">AtCoder</div>
                      </div>
                    </div>
                    <button
                      onClick={onClose}
                      className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
                    >
                      Connect Accounts in Settings
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <div className="text-sm text-gray-400 mb-4">
                  Showing {filteredProblems.length} problems
                  {hasActiveFilters() && (
                    <span className="ml-2 px-2 py-1 bg-blue-600/20 text-blue-400 rounded text-xs">
                      Filtered
                    </span>
                  )}
                </div>

                <div className="grid gap-3">
                  {filteredProblems.map((problem, idx) => (
                    <div
                      key={idx}
                      className="bg-gray-800/60 border border-gray-700 rounded-lg p-4 hover:bg-gray-800/80 transition-colors"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <div
                              className="px-2 py-1 rounded text-xs font-medium capitalize"
                              style={{
                                backgroundColor: `${getPlatformColor(
                                  problem.platform
                                )}20`,
                                color: getPlatformColor(problem.platform),
                                border: `1px solid ${getPlatformColor(
                                  problem.platform
                                )}40`,
                              }}
                            >
                              {problem.platform}
                            </div>
                            <div
                              className={`px-2 py-1 rounded text-xs font-medium border ${getVerdictColor(
                                problem.verdict
                              )}`}
                            >
                              {problem.verdict || "Unknown"}
                            </div>
                            <div
                              className={`text-xs font-medium ${getDifficultyColor(
                                problem.difficulty
                              )}`}
                            >
                              {problem.difficulty || "Unknown"}
                            </div>
                          </div>

                          <h3 className="text-white font-medium mb-1">
                            {problem.title ||
                              problem.problemId ||
                              "Unknown Problem"}
                          </h3>

                          {problem.problemId &&
                            problem.problemId !== problem.title && (
                              <div className="text-sm text-gray-400 mb-2">
                                ID: {problem.problemId}
                              </div>
                            )}

                          <div className="flex items-center gap-4 text-xs text-gray-400">
                            <span>📅 {formatDate(problem.date)}</span>
                            {problem.language &&
                              problem.language !== "unknown" && (
                                <span>💻 {problem.language}</span>
                              )}
                            {problem.rating && <span>⭐ {problem.rating}</span>}
                          </div>

                          {problem.tags && problem.tags.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1">
                              {problem.tags.slice(0, 5).map((tag, tagIdx) => (
                                <span
                                  key={tagIdx}
                                  className="px-1.5 py-0.5 bg-gray-700 text-gray-300 text-xs rounded"
                                >
                                  {tag}
                                </span>
                              ))}
                              {problem.tags.length > 5 && (
                                <span className="px-1.5 py-0.5 bg-gray-700 text-gray-300 text-xs rounded">
                                  +{problem.tags.length - 5} more
                                </span>
                              )}
                            </div>
                          )}
                        </div>

                        <div className="ml-4">
                          {problem.url && (
                            <a
                              href={problem.url}
                              target="_blank"
                              rel="noreferrer"
                              className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white text-sm rounded transition-colors"
                            >
                              View
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {isDemoData && (
                  <div className="mt-6 p-4 bg-blue-900/20 border border-blue-800/50 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-blue-400">ℹ️</span>
                      <span className="text-sm font-medium text-blue-300">
                        Demo Data
                      </span>
                    </div>
                    <p className="text-xs text-blue-200/80">
                      This is sample data from active competitive programmers.
                      Connect your own accounts to see your personal submission
                      history!
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function PlatformProblemHistory({ platform, token }) {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlatformProblems = async () => {
      setLoading(true);
      setError(null);

      try {
        let url = `http://localhost:5000/api/stats/problems?platform=${platform}&limit=10&days=60`;
        let headers = {
          "Content-Type": "application/json",
        };

        if (token) {
          headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, { headers });

        if (!response.ok) {
          throw new Error(`Failed to fetch ${platform} problems`);
        }

        const data = await response.json();
        console.log(`${platform} problems:`, data);

        if (data.problems && Array.isArray(data.problems)) {
          // Filter problems for this platform only
          const platformProblems = data.problems.filter(
            (p) => p.platform === platform
          );
          setProblems(platformProblems);
        } else {
          setProblems([]);
        }
      } catch (err) {
        console.error(`Error fetching ${platform} problems:`, err);
        setError(err.message);
        setProblems([]);
      } finally {
        setLoading(false);
      }
    };

    if (platform) {
      fetchPlatformProblems();
    }
  }, [platform, token]);

  const getPlatformColor = (platform) => {
    const colors = {
      leetcode: "#FFA116",
      codeforces: "#1F8ACB",
      atcoder: "#3F7FBF",
      codechef: "#5B4638",
    };
    return colors[platform] || "#6B7280";
  };

  const getVerdictColor = (verdict) => {
    const v = verdict?.toString().toUpperCase();
    if (v === "OK" || v === "AC" || v === "ACCEPTED") {
      return "bg-green-900 text-green-300 border-green-800";
    } else if (v === "WA" || v === "WRONG ANSWER") {
      return "bg-red-900 text-red-300 border-red-800";
    } else if (v === "TLE" || v === "TIME LIMIT EXCEEDED") {
      return "bg-yellow-900 text-yellow-300 border-yellow-800";
    } else {
      return "bg-gray-900 text-gray-300 border-gray-700";
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "text-green-400";
      case "medium":
        return "text-yellow-400";
      case "hard":
        return "text-red-400";
      default:
        return "text-gray-400";
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "Unknown";
    try {
      return new Date(dateStr).toLocaleString();
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="bg-gray-800/40 rounded-lg p-4">
      <h3 className="text-lg font-semibold mb-3 text-white capitalize">
        Recent {platform} Problems
      </h3>

      {loading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-gray-400">Loading problems...</span>
        </div>
      ) : error ? (
        <div className="text-center py-6">
          <p className="text-red-400 mb-2">Error loading problems</p>
          <p className="text-gray-500 text-sm">{error}</p>
        </div>
      ) : problems.length === 0 ? (
        <div className="text-center py-6">
          <p className="text-gray-400 mb-2">
            No recent {platform} problems found
          </p>
          <p className="text-gray-500 text-sm">
            Solve some problems to see them here!
          </p>
        </div>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {problems.map((problem, idx) => (
            <div
              key={idx}
              className="bg-gray-700/50 rounded-lg p-3 hover:bg-gray-700/70 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <div
                      className={`px-2 py-1 rounded text-xs font-medium border ${getVerdictColor(
                        problem.verdict
                      )}`}
                    >
                      {problem.verdict || "Unknown"}
                    </div>
                    <div
                      className={`text-xs font-medium ${getDifficultyColor(
                        problem.difficulty
                      )}`}
                    >
                      {problem.difficulty || "Unknown"}
                    </div>
                    {problem.rating && (
                      <div className="text-xs text-yellow-400">
                        ⭐ {problem.rating}
                      </div>
                    )}
                  </div>

                  <h4 className="text-white font-medium mb-1 text-sm">
                    {problem.title || problem.problemId || "Unknown Problem"}
                  </h4>

                  <div className="flex items-center gap-3 text-xs text-gray-400">
                    <span>📅 {formatDate(problem.date)}</span>
                    {problem.language && problem.language !== "unknown" && (
                      <span>💻 {problem.language}</span>
                    )}
                  </div>

                  {problem.tags && problem.tags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {problem.tags.slice(0, 3).map((tag, tagIdx) => (
                        <span
                          key={tagIdx}
                          className="px-1.5 py-0.5 bg-gray-600 text-gray-300 text-xs rounded"
                        >
                          {tag}
                        </span>
                      ))}
                      {problem.tags.length > 3 && (
                        <span className="px-1.5 py-0.5 bg-gray-600 text-gray-300 text-xs rounded">
                          +{problem.tags.length - 3}
                        </span>
                      )}
                    </div>
                  )}
                </div>

                <div className="ml-3">
                  {problem.url && (
                    <a
                      href={problem.url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-2 py-1 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded transition-colors"
                    >
                      View
                    </a>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function PlatformIcon({ platform }) {
  const icons = {
    leetcode: (
      <svg
        className="w-6 h-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M15 3l-9 9 9 9" />
        <path d="M21 3l-9 9 9 9" />
      </svg>
    ),
    codeforces: (
      <svg
        className="w-6 h-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <rect x="3" y="3" width="4" height="18" />
        <rect x="10" y="6" width="4" height="15" />
        <rect x="17" y="9" width="4" height="12" />
      </svg>
    ),
    atcoder: (
      <svg
        className="w-6 h-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <path d="M3 20h18" />
        <path d="M7 20V8l5-3 5 3v12" />
      </svg>
    ),
    codechef: (
      <svg
        className="w-6 h-6"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      >
        <circle cx="12" cy="12" r="9" />
        <path d="M8 15c1.333-1.333 2.667-1.333 4 0s2.667 1.333 4 0" />
        <path d="M9 10h.01M15 10h.01" />
      </svg>
    ),
  };
  return icons[platform] || icons.leetcode;
}

function PlatformDetails({ details, color, platform }) {
  if (!details.connected) {
    return (
      <div className="p-8 text-center">
        <p className="text-gray-400 mb-4">
          This platform account is not connected.
        </p>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg">
          Connect Account
        </button>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Overview Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          label="Total Solved"
          value={details.totalSolved || 0}
          color={color}
          icon="🎯"
        />
        <StatCard
          label="Current Rating"
          value={details.rating || 0}
          color={color}
          icon="⭐"
        />
        <StatCard
          label="Contest Count"
          value={details.contestCount || 0}
          color={color}
          icon="🏆"
        />
        <StatCard
          label="Current Streak"
          value={`${details.streak || 0} days`}
          color={color}
          icon="🔥"
        />
      </div>

      {/* Difficulty Breakdown */}
      <div className="bg-gray-800/40 rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3 text-white">
          Problem Difficulty Breakdown
        </h3>
        <div className="grid grid-cols-3 gap-4">
          <DifficultyCard
            label="Easy"
            count={details.easy || 0}
            color="#10B981"
          />
          <DifficultyCard
            label="Medium"
            count={details.medium || 0}
            color="#F59E0B"
          />
          <DifficultyCard
            label="Hard"
            count={details.hard || 0}
            color="#EF4444"
          />
        </div>
      </div>

      {/* Strengths & Badges */}
      <div className="grid md:grid-cols-2 gap-6">
        {details.strengths && details.strengths.length > 0 && (
          <div className="bg-gray-800/40 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-3 text-white">Strengths</h3>
            <div className="flex flex-wrap gap-2">
              {details.strengths.map((strength, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 rounded-full text-sm font-medium border"
                  style={{
                    backgroundColor: `${color}20`,
                    borderColor: color,
                    color,
                  }}
                >
                  {strength}
                </span>
              ))}
            </div>
          </div>
        )}

        {details.badges && details.badges.length > 0 && (
          <div className="bg-gray-800/40 rounded-lg p-4">
            <h3 className="text-lg font-semibold mb-3 text-white">
              Achievements
            </h3>
            <div className="space-y-2">
              {details.badges.map((badge, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-3 p-2 bg-gray-700/50 rounded"
                >
                  <span className="text-lg">🏅</span>
                  <div>
                    <div className="font-medium text-white">{badge.name}</div>
                    <div className="text-sm text-gray-400">
                      {badge.description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Problem History for this Platform */}
      <PlatformProblemHistory
        platform={platform}
        token={localStorage.getItem("session_token")}
      />

      {/* Recent Activity */}
      {details.recentSubmissions && details.recentSubmissions.length > 0 && (
        <div className="bg-gray-800/40 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-3 text-white">
            Recent Submissions (Legacy)
          </h3>
          <div className="space-y-2">
            {details.recentSubmissions.slice(0, 5).map((submission, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-2 bg-gray-700/50 rounded text-sm"
              >
                <div className="text-white font-medium">
                  {submission.problem}
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${
                      submission.verdict === "AC"
                        ? "bg-green-900 text-green-300"
                        : "bg-red-900 text-red-300"
                    }`}
                  >
                    {submission.verdict}
                  </span>
                  <span className="text-gray-400">{submission.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Contest History */}
      {details.contestHistory && details.contestHistory.length > 0 && (
        <div className="bg-gray-800/40 rounded-lg p-4">
          <h3 className="text-lg font-semibold mb-3 text-white">
            Recent Contests
          </h3>
          <div className="space-y-2">
            {details.contestHistory.slice(0, 5).map((contest, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-2 bg-gray-700/50 rounded text-sm"
              >
                <div className="text-white font-medium">{contest.contest}</div>
                <div className="flex items-center gap-2">
                  <span className="text-gray-300">Rank: {contest.rank}</span>
                  {contest.rating_change && (
                    <span
                      className={`px-2 py-1 rounded text-xs font-medium ${
                        contest.rating_change.startsWith("+")
                          ? "bg-green-900 text-green-300"
                          : "bg-red-900 text-red-300"
                      }`}
                    >
                      {contest.rating_change}
                    </span>
                  )}
                  <span className="text-gray-400">{contest.date}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function DifficultyCard({ label, count, color }) {
  return (
    <div className="text-center">
      <div className="text-2xl font-bold mb-1" style={{ color }}>
        {count}
      </div>
      <div className="text-sm text-gray-400">{label}</div>
      <div
        className="w-full h-2 rounded-full mt-2"
        style={{ backgroundColor: `${color}30` }}
      >
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{
            backgroundColor: color,
            width: `${Math.min(100, (count / Math.max(count, 50)) * 100)}%`,
          }}
        />
      </div>
    </div>
  );
}

function TopProblems() {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [availableTopics, setAvailableTopics] = useState([]);
  const [displayCount, setDisplayCount] = useState(6);
  const [filters, setFilters] = useState({
    platform: "all",
    difficulty: "all",
    category: "all",
    topic: "all",
  });
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    fetchTopProblems();
  }, [filters]);

  const fetchTopProblems = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        platform: filters.platform,
        difficulty: filters.difficulty,
        category: filters.category,
        topic: filters.topic,
        limit: "100",
      });

      const response = await fetch(
        `http://localhost:5000/api/stats/top-problems?${params}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch top problems");
      }

      const data = await response.json();
      setProblems(data.problems || []);
      setAvailableTopics(data.availableTopics || []);
    } catch (err) {
      console.error("Error fetching top problems:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const resetFilters = () => {
    setFilters({
      platform: "all",
      difficulty: "all",
      category: "all",
      topic: "all",
    });
  };

  const getPlatformColor = (platform) => {
    const colors = {
      leetcode: "#FFA116",
      codeforces: "#1F8ACB",
      atcoder: "#3F7FBF",
    };
    return colors[platform] || "#6B7280";
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty?.toLowerCase()) {
      case "easy":
        return "text-green-400 bg-green-400/10 border-green-400/20";
      case "medium":
        return "text-yellow-400 bg-yellow-400/10 border-yellow-400/20";
      case "hard":
        return "text-red-400 bg-red-400/10 border-red-400/20";
      default:
        return "text-gray-400 bg-gray-400/10 border-gray-400/20";
    }
  };

  const hasActiveFilters = () => {
    return (
      filters.platform !== "all" ||
      filters.difficulty !== "all" ||
      filters.category !== "all" ||
      filters.topic !== "all"
    );
  };

  const displayedProblems = problems.slice(0, displayCount);
  const canShowMore = displayCount < problems.length;

  return (
    <div className="mt-6">
      {/* Modern Header */}
      <div className="bg-gradient-to-r from-purple-900/20 via-blue-900/20 to-cyan-900/20 border border-purple-500/20 rounded-2xl p-8 mb-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-xl flex items-center justify-center">
              <span className="text-2xl">🎯</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white mb-1">
                Essential Problem Sets
              </h2>
              <p className="text-purple-200/80">
                Master competitive programming with these curated challenges
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`px-4 py-2 rounded-xl border transition-all duration-200 flex items-center gap-2 font-medium ${
                showFilters
                  ? "bg-blue-500 border-blue-400 text-white shadow-lg shadow-blue-500/25"
                  : "bg-white/5 border-white/10 text-white hover:bg-white/10 hover:border-white/20"
              }`}
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"
                />
              </svg>
              Filters
              {hasActiveFilters() && (
                <span className="bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
                  !
                </span>
              )}
            </button>

            <div className="text-sm text-purple-200/60">
              {loading ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
                  Loading...
                </span>
              ) : (
                `${problems.length} problems available`
              )}
            </div>
          </div>
        </div>

        {/* Enhanced Filter Controls */}
        {showFilters && (
          <div className="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Platform Filter */}
              <div>
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Platform
                </label>
                <select
                  value={filters.platform}
                  onChange={(e) => updateFilter("platform", e.target.value)}
                  className="w-full bg-black/40 border border-white/20 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                >
                  <option value="all">All Platforms</option>
                  <option value="leetcode">LeetCode</option>
                  <option value="codeforces">Codeforces</option>
                  <option value="atcoder">AtCoder</option>
                </select>
              </div>

              {/* Difficulty Filter */}
              <div>
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Difficulty
                </label>
                <select
                  value={filters.difficulty}
                  onChange={(e) => updateFilter("difficulty", e.target.value)}
                  className="w-full bg-black/40 border border-white/20 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                >
                  <option value="all">All Difficulties</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>

              {/* Category Filter */}
              <div>
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Category
                </label>
                <select
                  value={filters.category}
                  onChange={(e) => updateFilter("category", e.target.value)}
                  className="w-full bg-black/40 border border-white/20 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                >
                  <option value="all">All Categories</option>
                  <option value="classic">Classic Problems</option>
                  <option value="interview">Interview Prep</option>
                  <option value="contest">Contest Problems</option>
                  <option value="beginner">Beginner Friendly</option>
                </select>
              </div>

              {/* Topic Filter */}
              <div>
                <label className="block text-sm font-medium text-purple-200 mb-2">
                  Topic
                </label>
                <select
                  value={filters.topic}
                  onChange={(e) => updateFilter("topic", e.target.value)}
                  className="w-full bg-black/40 border border-white/20 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                >
                  <option value="all">All Topics</option>
                  {availableTopics.map((topic, idx) => (
                    <option key={idx} value={topic}>
                      {topic}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Filter Actions */}
            <div className="flex items-center justify-between mt-6 pt-4 border-t border-white/10">
              <div className="text-sm text-purple-200/70">
                {hasActiveFilters() ? (
                  <span className="flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-400 rounded-full"></span>
                    Filters active
                  </span>
                ) : (
                  "No filters applied"
                )}
              </div>
              <div className="flex gap-3">
                {hasActiveFilters() && (
                  <button
                    onClick={resetFilters}
                    className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors text-sm font-medium"
                  >
                    Reset Filters
                  </button>
                )}
                <button
                  onClick={() => setShowFilters(false)}
                  className="px-4 py-2 bg-purple-500 hover:bg-purple-400 text-white rounded-lg transition-colors text-sm font-medium"
                >
                  Hide Filters
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="flex flex-col items-center">
            <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <div className="text-white font-medium">
              Loading awesome problems...
            </div>
            <div className="text-purple-200/60 text-sm mt-1">
              Finding the best challenges for you
            </div>
          </div>
        </div>
      ) : error ? (
        <div className="text-center py-16">
          <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">⚠️</span>
          </div>
          <div className="text-red-400 mb-2 font-medium">
            Oops! Something went wrong
          </div>
          <div className="text-sm text-gray-400 mb-6 max-w-md mx-auto">
            {error}
          </div>
          <button
            onClick={fetchTopProblems}
            className="px-6 py-3 bg-red-500 hover:bg-red-400 text-white rounded-xl font-medium transition-all duration-200 shadow-lg hover:shadow-red-500/25"
          >
            Try Again
          </button>
        </div>
      ) : problems.length === 0 ? (
        <div className="text-center py-16">
          <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">🔍</span>
          </div>
          <div className="text-white mb-2 font-medium">No problems found</div>
          <div className="text-sm text-gray-400 mb-6 max-w-md mx-auto">
            No problems match your current filters. Try adjusting your criteria.
          </div>
          <button
            onClick={resetFilters}
            className="px-6 py-3 bg-blue-500 hover:bg-blue-400 text-white rounded-xl font-medium transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div>
          {/* Problem Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {displayedProblems.map((problem, idx) => (
              <div
                key={idx}
                className="group relative bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6 hover:border-purple-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/10 hover:-translate-y-1"
              >
                {/* Platform & Difficulty Badges */}
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <div
                      className="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wide"
                      style={{
                        backgroundColor: `${getPlatformColor(
                          problem.platform
                        )}20`,
                        color: getPlatformColor(problem.platform),
                        border: `1px solid ${getPlatformColor(
                          problem.platform
                        )}30`,
                      }}
                    >
                      {problem.platform}
                    </div>
                    <div
                      className={`px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyColor(
                        problem.difficulty
                      )}`}
                    >
                      {problem.difficulty}
                    </div>
                  </div>

                  {problem.rating && (
                    <div className="flex items-center gap-1 text-yellow-400 text-sm font-medium">
                      <span>⭐</span>
                      <span>{problem.rating}</span>
                    </div>
                  )}
                </div>

                {/* Problem Title */}
                <h3 className="text-white font-bold mb-3 text-lg leading-tight group-hover:text-purple-200 transition-colors">
                  {problem.title}
                </h3>

                {/* Description */}
                <p
                  className="text-gray-300 text-sm mb-4 leading-relaxed"
                  style={{
                    display: "-webkit-box",
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: "vertical",
                    overflow: "hidden",
                  }}
                >
                  {problem.description}
                </p>

                {/* Tags */}
                {problem.tags && problem.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {problem.tags.slice(0, 3).map((tag, tagIdx) => (
                      <span
                        key={tagIdx}
                        className="px-2 py-1 bg-gray-700/50 text-gray-300 text-xs rounded-lg border border-gray-600/50 hover:bg-purple-600/20 hover:border-purple-500/30 transition-colors cursor-pointer"
                        onClick={() => updateFilter("topic", tag)}
                        title={`Filter by ${tag}`}
                      >
                        {tag}
                      </span>
                    ))}
                    {problem.tags.length > 3 && (
                      <span className="px-2 py-1 bg-gray-700/50 text-gray-400 text-xs rounded-lg border border-gray-600/50">
                        +{problem.tags.length - 3} more
                      </span>
                    )}
                  </div>
                )}

                {/* Stats & Action */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4 text-xs text-gray-400">
                    <span className="flex items-center gap-1">
                      <span>👥</span>
                      <span>{problem.solveCount}</span>
                    </span>
                    <span className="flex items-center gap-1">
                      <span>✓</span>
                      <span>{problem.acceptance}</span>
                    </span>
                  </div>

                  <a
                    href={problem.url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-400 hover:to-blue-400 text-white text-sm font-medium rounded-xl transition-all duration-200 shadow-lg hover:shadow-purple-500/25 transform hover:scale-105"
                  >
                    Solve Now
                  </a>
                </div>
              </div>
            ))}
          </div>

          {/* Load More Slider */}
          {canShowMore && (
            <div className="mt-8 bg-gradient-to-r from-gray-800/30 to-gray-900/30 rounded-2xl p-6 border border-gray-700/30">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
                    <span className="text-white text-lg">📊</span>
                  </div>
                  <div>
                    <div className="text-white font-medium">
                      Show More Problems
                    </div>
                    <div className="text-gray-400 text-sm">
                      Displaying {displayCount} of {problems.length} problems
                    </div>
                  </div>
                </div>
                <div className="text-purple-300 text-sm font-medium">
                  {Math.round((displayCount / problems.length) * 100)}% shown
                </div>
              </div>

              {/* Slider */}
              <div className="space-y-4">
                <input
                  type="range"
                  min="6"
                  max={problems.length}
                  step="6"
                  value={displayCount}
                  onChange={(e) => setDisplayCount(parseInt(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
                  style={{
                    background: `linear-gradient(to right, #8B5CF6 0%, #3B82F6 ${
                      (displayCount / problems.length) * 100
                    }%, #374151 ${
                      (displayCount / problems.length) * 100
                    }%, #374151 100%)`,
                  }}
                />

                {/* Quick Action Buttons */}
                <div className="flex items-center justify-center gap-3">
                  <button
                    onClick={() =>
                      setDisplayCount(Math.max(6, displayCount - 6))
                    }
                    disabled={displayCount <= 6}
                    className="px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:bg-gray-800 disabled:text-gray-500 text-white rounded-lg transition-colors text-sm font-medium disabled:cursor-not-allowed"
                  >
                    Show Less
                  </button>
                  <button
                    onClick={() =>
                      setDisplayCount(
                        Math.min(problems.length, displayCount + 6)
                      )
                    }
                    disabled={displayCount >= problems.length}
                    className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-400 hover:to-blue-400 disabled:from-gray-700 disabled:to-gray-700 disabled:text-gray-500 text-white rounded-lg transition-all text-sm font-medium disabled:cursor-not-allowed"
                  >
                    Show More
                  </button>
                  <button
                    onClick={() => setDisplayCount(problems.length)}
                    disabled={displayCount >= problems.length}
                    className="px-4 py-2 bg-white/10 hover:bg-white/20 disabled:bg-gray-800 disabled:text-gray-500 text-white rounded-lg transition-colors text-sm font-medium disabled:cursor-not-allowed"
                  >
                    Show All
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function TextField({ label, value, onChange, placeholder }) {
  return (
    <label className="block">
      <div className="mb-1 text-gray-300">{label}</div>
      <input
        className="w-full px-3 py-2 rounded bg-gray-900 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-600/40"
        value={value || ""}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </label>
  );
}

function OverviewStatCard({ label, value }) {
  return (
    <div className="bg-gray-800 border border-gray-700 rounded p-3">
      <div className="text-gray-400 text-sm">{label}</div>
      <div className="text-lg font-semibold mt-1">{value}</div>
    </div>
  );
}

function StatCard({ label, value, color, icon }) {
  return (
    <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4 text-center">
      {icon && <div className="text-2xl mb-2">{icon}</div>}
      <div className="text-gray-400 text-sm mb-1">{label}</div>
      <div className="text-xl font-bold" style={{ color: color || "#fff" }}>
        {value}
      </div>
    </div>
  );
}

function Heatmap({ days }) {
  const bgFor = (c) => {
    if (!c || c <= 0) return "bg-gray-800";
    if (c === 1) return "bg-emerald-900";
    if (c === 2) return "bg-emerald-800";
    if (c === 3) return "bg-emerald-700";
    return "bg-emerald-600";
  };

  // Ensure we have valid data
  const validDays = Array.isArray(days) ? days : [];

  // Generate date range for the past 91 days (13 weeks)
  const today = new Date();
  const startDate = new Date(today);
  startDate.setDate(today.getDate() - 90);

  const dateMap = {};
  validDays.forEach((day) => {
    if (day && day.date) {
      dateMap[day.date] = day.count || 0;
    }
  });

  // Create 13 weeks x 7 days grid
  const weeks = [];
  for (let week = 0; week < 13; week++) {
    const weekDays = [];
    for (let day = 0; day < 7; day++) {
      const currentDate = new Date(startDate);
      currentDate.setDate(startDate.getDate() + week * 7 + day);
      const dateStr = currentDate.toISOString().split("T")[0];
      const count = dateMap[dateStr] || 0;

      weekDays.push({
        date: dateStr,
        count: count,
        displayDate: currentDate.toLocaleDateString(),
      });
    }
    weeks.push(weekDays);
  }

  if (validDays.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        <p>No activity data available</p>
        <p className="text-sm mt-1">
          Connect your accounts to see daily activity
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <div className="inline-grid grid-rows-7 grid-flow-col gap-1">
        {weeks.map((week, wi) => (
          <div key={wi} className="contents">
            {week.map((cell, di) => (
              <div
                key={`${wi}-${di}`}
                title={`${cell.displayDate}: ${cell.count} problems solved`}
                className={`w-3.5 h-3.5 rounded ${bgFor(
                  cell.count
                )} border border-gray-700/50 hover:border-gray-500 transition-colors cursor-pointer`}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="mt-2 flex items-center justify-between text-xs text-gray-400">
        <span>Past 13 weeks</span>
        <div className="flex items-center gap-2">
          <span>Less</span>
          <div className="flex gap-1">
            <div className="w-2.5 h-2.5 rounded bg-gray-800 border border-gray-700"></div>
            <div className="w-2.5 h-2.5 rounded bg-emerald-900 border border-gray-700"></div>
            <div className="w-2.5 h-2.5 rounded bg-emerald-800 border border-gray-700"></div>
            <div className="w-2.5 h-2.5 rounded bg-emerald-700 border border-gray-700"></div>
            <div className="w-2.5 h-2.5 rounded bg-emerald-600 border border-gray-700"></div>
          </div>
          <span>More</span>
        </div>
      </div>
    </div>
  );
}

function TopicBadge({ name, level }) {
  const color =
    level === "strong"
      ? "bg-emerald-900 text-emerald-300 border-emerald-800"
      : level === "good"
      ? "bg-sky-900 text-sky-300 border-sky-800"
      : level === "improving"
      ? "bg-amber-900 text-amber-300 border-amber-800"
      : "bg-rose-900 text-rose-300 border-rose-800";
  return (
    <span className={`px-2 py-1 rounded border text-[11px] ${color}`}>
      {name}
    </span>
  );
}

function CalendarStrip({ contests, next7Only, platformFilter, searchFilter }) {
  const days = Array.from({ length: 7 }, (_, i) => {
    const d = new Date();
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + i);
    return d;
  });
  const filtered = (c) => {
    if (platformFilter !== "all" && c.platform !== platformFilter) return false;
    if (!c.name.toLowerCase().includes(searchFilter.toLowerCase()))
      return false;
    return true;
  };
  const counts = days.map((d) => {
    const next = new Date(d);
    next.setDate(next.getDate() + 1);
    const n = contests.filter((c) => {
      const cs = new Date(c.start);
      return filtered(c) && cs >= d && cs < next;
    }).length;
    return n;
  });
  return (
    <div className="mb-3 flex items-center gap-2 text-xs text-gray-300">
      {days.map((d, i) => (
        <div key={i} className="flex flex-col items-center">
          <div
            className={`w-6 h-6 rounded border ${
              counts[i] > 0
                ? "bg-emerald-800 border-emerald-700"
                : "bg-gray-800 border-gray-700"
            }`}
            title={`${d.toDateString()}: ${counts[i]} contests`}
          />
          <div className="mt-1 text-[10px] text-gray-400">
            {d.toLocaleDateString(undefined, { weekday: "short" })}
          </div>
        </div>
      ))}
    </div>
  );
}

function LinkedAccounts({
  accounts,
  onHover,
  onLeave,
  stats,
  onPlatformClick,
}) {
  const items = [
    {
      key: "leetcode",
      label: "LeetCode",
      color: "#FFA116",
      icon: (
        <svg
          className="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M15 3l-9 9 9 9" />
          <path d="M21 3l-9 9 9 9" />
        </svg>
      ),
      url: (u) => `https://leetcode.com/${u}/`,
    },
    {
      key: "codeforces",
      label: "Codeforces",
      color: "#1F8ACB",
      icon: (
        <svg
          className="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <rect x="3" y="3" width="4" height="18" />
          <rect x="10" y="6" width="4" height="15" />
          <rect x="17" y="9" width="4" height="12" />
        </svg>
      ),
      url: (u) => `https://codeforces.com/profile/${u}`,
    },
    {
      key: "atcoder",
      label: "AtCoder",
      color: "#3F7FBF",
      icon: (
        <svg
          className="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M3 20h18" />
          <path d="M7 20V8l5-3 5 3v12" />
        </svg>
      ),
      url: (u) => `https://atcoder.jp/users/${u}`,
    },
    {
      key: "codechef",
      label: "CodeChef",
      color: "#5B4638",
      icon: (
        <svg
          className="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="9" />
          <path d="M8 15c1.333-1.333 2.667-1.333 4 0s2.667 1.333 4 0" />
          <path d="M9 10h.01M15 10h.01" />
        </svg>
      ),
      url: (u) => `https://www.codechef.com/users/${u}`,
    },
  ];

  return (
    <div>
      <div className="text-lg font-semibold mb-3">Platform Statistics</div>
      <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4">
        {items.map((it, i) => {
          const username = accounts?.[it.key];
          const platformStats = stats?.perPlatform?.[it.key];
          const isConnected = username && username.length > 0;

          return (
            <div
              key={i}
              className={`group bg-gray-800/60 border transition-all duration-500 ease-out rounded-lg p-4 text-center cursor-pointer transform hover:scale-105 hover:-translate-y-1 hover:shadow-xl ${
                isConnected
                  ? "border-gray-600 hover:border-gray-500 hover:bg-gray-800/80"
                  : "border-gray-700 hover:border-gray-600"
              }`}
              style={{
                boxShadow: isConnected ? `0 4px 20px ${it.color}20` : "none",
                transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
              }}
              onMouseEnter={() => onHover && onHover(it.key)}
              onMouseLeave={() => onLeave && onLeave()}
              onClick={() =>
                isConnected && onPlatformClick && onPlatformClick(it.key)
              }
              title={
                isConnected
                  ? `Click to view detailed ${it.label} stats`
                  : `${it.label} account not connected`
              }
            >
              <div
                className="mx-auto w-12 h-12 rounded-full border-2 flex items-center justify-center transition-all duration-300 group-hover:scale-110"
                style={{
                  backgroundColor: isConnected ? `${it.color}20` : "#1F2937",
                  borderColor: isConnected ? it.color : "#374151",
                  color: isConnected ? it.color : "#9CA3AF",
                  transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                }}
              >
                {it.icon}
              </div>

              <div className="mt-3">
                <div className="text-sm font-medium text-gray-200">
                  {it.label}
                </div>
                {isConnected ? (
                  <div className="mt-2 space-y-1">
                    <a
                      href={it.url(username)}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-block text-blue-300 hover:text-blue-200 text-xs font-medium"
                      title={`Open ${it.label} profile`}
                      onClick={(e) => e.stopPropagation()}
                    >
                      @{username}
                    </a>
                    {platformStats && (
                      <div className="text-xs text-gray-400 space-y-0.5">
                        <div>{platformStats.totalSolved || 0} problems</div>
                        <div className="flex items-center justify-center gap-1">
                          <span className="inline-block w-1.5 h-1.5 rounded-full bg-green-400"></span>
                          <span>Rating: {platformStats.rating || 0}</span>
                        </div>
                      </div>
                    )}
                    <div className="mt-2">
                      <button
                        className={`text-xs px-2 py-1 rounded-full border transition-colors`}
                        style={{
                          backgroundColor: `${it.color}20`,
                          borderColor: it.color,
                          color: it.color,
                        }}
                      >
                        View Details
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-2">
                    <div className="text-xs text-gray-500 mb-2">
                      Not connected
                    </div>
                    <button className="text-xs px-2 py-1 rounded-full bg-gray-700 border border-gray-600 text-gray-300 hover:bg-gray-600">
                      Connect Account
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function CodeSpaceTab() {
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [showCodeEditor, setShowCodeEditor] = useState(false);
  const [code, setCode] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("javascript");
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState(null);
  const [activeTab, setActiveTab] = useState("description");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submissionResult, setSubmissionResult] = useState(null);

  const languages = [
    { id: "javascript", name: "JavaScript", template: "// Write your solution here\nfunction solution() {\n    \n}" },
    { id: "python", name: "Python", template: "# Write your solution here\ndef solution():\n    pass" },
    { id: "cpp", name: "C++", template: "// Write your solution here\n#include <iostream>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}" },
    { id: "java", name: "Java", template: "// Write your solution here\npublic class Solution {\n    public static void main(String[] args) {\n        \n    }\n}" }
  ];

  const sampleProblems = [
    {
      id: 1,
      title: "Two Sum",
      difficulty: "Easy",
      platform: "leetcode",
      url: "https://leetcode.com/problems/two-sum/",
      description: `Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.`,
      examples: [
        { input: "nums = [2,7,11,15], target = 9", output: "[0,1]", explanation: "Because nums[0] + nums[1] == 9, we return [0, 1]." },
        { input: "nums = [3,2,4], target = 6", output: "[1,2]" }
      ],
      constraints: ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Only one valid answer exists."],
      testCases: [{ input: "[2,7,11,15], 9", expected: "[0,1]" }, { input: "[3,2,4], 6", expected: "[1,2]" }]
    },
    {
      id: 2,
      title: "Valid Parentheses",
      difficulty: "Easy",
      platform: "leetcode",
      url: "https://leetcode.com/problems/valid-parentheses/",
      description: `Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.`,
      examples: [{ input: 's = "()"', output: "true" }, { input: 's = "()[]{}"', output: "true" }],
      constraints: ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'."],
      testCases: [{ input: '"()"', expected: "true" }, { input: '"()[]{}"', expected: "true" }]
    }
  ];

  const openCodeEditor = (problem) => {
    setSelectedProblem(problem);
    setShowCodeEditor(true);
    setCode(languages.find(lang => lang.id === selectedLanguage)?.template || "");
    setTestResults(null);
    setSubmissionResult(null);
  };

  const closeCodeEditor = () => {
    setShowCodeEditor(false);
    setSelectedProblem(null);
    setCode("");
    setTestResults(null);
    setSubmissionResult(null);
  };

  const runCode = async () => {
    setIsRunning(true);
    setTimeout(() => {
      const passedTests = Math.floor(Math.random() * selectedProblem.testCases.length) + 1;
      setTestResults({
        passed: passedTests,
        total: selectedProblem.testCases.length,
        details: selectedProblem.testCases.map((test, idx) => ({
          input: test.input,
          expected: test.expected,
          actual: idx < passedTests ? test.expected : "Wrong Answer",
          status: idx < passedTests ? "PASS" : "FAIL"
        }))
      });
      setIsRunning(false);
    }, 2000);
  };

  const submitCode = async () => {
    setIsSubmitting(true);
    setTimeout(() => {
      const success = Math.random() > 0.3;
      setSubmissionResult({
        success,
        message: success ? "Accepted! Your solution passed all test cases." : "Wrong Answer on test case 5 of 15.",
        runtime: success ? `${Math.floor(Math.random() * 100) + 50}ms` : null,
        memory: success ? `${(Math.random() * 20 + 10).toFixed(1)}MB` : null
      });
      setIsSubmitting(false);
    }, 3000);
  };

  if (showCodeEditor && selectedProblem) {
    return (
      <div className="h-screen max-h-screen overflow-hidden">
        {/* Code Editor Header */}
        <div className="bg-gradient-to-r from-gray-800/60 to-gray-700/60 border border-gray-600/50 rounded-t-2xl p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowCodeEditor(false)}
                className="p-2 rounded-lg hover:bg-white/10 text-gray-300 hover:text-white transition-colors"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div>
                <h2 className="text-lg font-bold text-white">{selectedProblem.title}</h2>
                <div className="flex items-center gap-2 text-sm">
                  <span className={`px-2 py-1 rounded text-xs ${
                    selectedProblem.difficulty === "Easy" ? "bg-green-500/20 text-green-400" :
                    selectedProblem.difficulty === "Medium" ? "bg-yellow-500/20 text-yellow-400" :
                    "bg-red-500/20 text-red-400"
                  }`}>
                    {selectedProblem.difficulty}
                  </span>
                  <span className="text-gray-400">{selectedProblem.platform}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <a
                href={selectedProblem.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm transition-colors"
              >
                Open in {selectedProblem.platform}
              </a>
            </div>
          </div>
        </div>

        {/* Editor Layout */}
        <div className="flex h-full bg-gray-900">
          {/* Problem Description Panel */}
          <div className="w-1/2 border-r border-gray-700 flex flex-col">
            {/* Description Tabs */}
            <div className="flex border-b border-gray-700">
              {["description", "examples", "constraints"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-4 py-3 text-sm font-medium transition-colors ${
                    activeTab === tab
                      ? "bg-gray-800 text-white border-b-2 border-blue-500"
                      : "text-gray-400 hover:text-white hover:bg-gray-800/50"
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {/* Description Content */}
            <div className="flex-1 p-6 overflow-y-auto">
              {activeTab === "description" && (
                <div className="text-gray-300 space-y-4">
                  <div className="whitespace-pre-line">{selectedProblem.description}</div>
                </div>
              )}
              
              {activeTab === "examples" && (
                <div className="space-y-4">
                  {selectedProblem.examples.map((example, idx) => (
                    <div key={idx} className="bg-gray-800/50 rounded-lg p-4">
                      <div className="text-sm font-medium text-white mb-2">Example {idx + 1}:</div>
                      <div className="space-y-2 text-sm">
                        <div><span className="text-gray-400">Input:</span> <code className="bg-gray-700 px-2 py-1 rounded">{example.input}</code></div>
                        <div><span className="text-gray-400">Output:</span> <code className="bg-gray-700 px-2 py-1 rounded">{example.output}</code></div>
                        {example.explanation && (
                          <div><span className="text-gray-400">Explanation:</span> {example.explanation}</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
              
              {activeTab === "constraints" && (
                <div className="space-y-2">
                  {selectedProblem.constraints.map((constraint, idx) => (
                    <div key={idx} className="text-gray-300 text-sm flex items-start gap-2">
                      <span className="text-blue-400 mt-1">•</span>
                      <code className="bg-gray-800 px-2 py-1 rounded text-xs">{constraint}</code>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Code Editor Panel */}
          <div className="w-1/2 flex flex-col">
            {/* Editor Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <select
                  value={selectedLanguage}
                  onChange={(e) => {
                    setSelectedLanguage(e.target.value);
                    setCode(languages.find(lang => lang.id === e.target.value)?.template || "");
                  }}
                  className="bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm"
                >
                  {languages.map(lang => (
                    <option key={lang.id} value={lang.id}>{lang.name}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={runCode}
                  disabled={isRunning}
                  className="px-4 py-2 bg-green-600 hover:bg-green-500 disabled:bg-green-700 disabled:cursor-not-allowed text-white rounded-lg text-sm transition-colors flex items-center gap-2"
                >
                  {isRunning ? (
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h1m4 0h1m6-4a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                  Run
                </button>
                <button
                  onClick={submitCode}
                  disabled={isRunning}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-700 disabled:cursor-not-allowed text-white rounded-lg text-sm transition-colors"
                >
                  Submit
                </button>
              </div>
            </div>

            {/* Code Editor */}
            <div className="flex-1 relative">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full h-full p-4 bg-gray-900 text-white font-mono text-sm resize-none focus:outline-none"
                style={{ fontFamily: 'Consolas, "Courier New", monospace' }}
                spellCheck={false}
              />
            </div>

            {/* Test Results */}
            {testResults && (
              <div className="border-t border-gray-700 p-4 max-h-48 overflow-y-auto bg-gray-800/50">
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <h4 className="text-white font-semibold">Test Results</h4>
                    <span className={`px-2 py-1 rounded text-sm ${
                      testResults.passed === testResults.total
                        ? "bg-green-500/20 text-green-400"
                        : "bg-red-500/20 text-red-400"
                    }`}>
                      {testResults.passed}/{testResults.total} Passed
                    </span>
                  </div>
                  
                  <div className="space-y-2">
                    {testResults.details.map((result, idx) => (
                      <div key={idx} className="bg-gray-700/50 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-white text-sm">Test Case {idx + 1}</span>
                          <span className={`px-2 py-1 rounded text-xs ${
                            result.status === "PASS" 
                              ? "bg-green-500/20 text-green-400" 
                              : "bg-red-500/20 text-red-400"
                          }`}>
                            {result.status}
                          </span>
                        </div>
                        <div className="font-mono text-xs space-y-1 text-gray-300">
                          <div><span className="text-blue-400">Input:</span> {result.input}</div>
                          <div><span className="text-green-400">Expected:</span> {result.expected}</div>
                          <div><span className="text-yellow-400">Actual:</span> {result.actual}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {submissionResult && (
              <div className="border-t border-gray-700 p-4 bg-gray-800/50">
                <div className={`p-4 rounded-lg ${
                  submissionResult.success
                    ? "bg-green-500/20 border border-green-500/30"
                    : "bg-red-500/20 border border-red-500/30"
                }`}>
                  <div className={`font-semibold mb-2 ${
                    submissionResult.success ? "text-green-400" : "text-red-400"
                  }`}>
                    {submissionResult.success ? "✓ Accepted" : "✗ Wrong Answer"}
                  </div>
                  <div className="text-gray-300 text-sm mb-3">{submissionResult.message}</div>
                  {submissionResult.success && (
                    <div className="flex gap-4 text-xs">
                      <span className="text-blue-400">Runtime: {submissionResult.runtime}</span>
                      <span className="text-purple-400">Memory: {submissionResult.memory}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Main CodeSpace View (Problem List)
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-900/20 via-blue-900/20 to-purple-900/20 border border-green-500/20 rounded-2xl p-8">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center">
            <span className="text-2xl">💻</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white mb-1">
              CodeSpace - Practice Arena
            </h2>
            <p className="text-green-200/80">
              Practice coding problems with our integrated code editor and test runner
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-green-400">✨</span>
              <span className="font-medium text-white">Multi-Language Support</span>
            </div>
            <p className="text-sm text-gray-400">JavaScript, Python, C++, Java</p>
          </div>
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-blue-400">🚀</span>
              <span className="font-medium text-white">Real-time Testing</span>
            </div>
            <p className="text-sm text-gray-400">Run and validate your code instantly</p>
          </div>
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-purple-400">📊</span>
              <span className="font-medium text-white">Submission System</span>
            </div>
            <p className="text-sm text-gray-400">Submit and get detailed feedback</p>
          </div>
        </div>
      </div>

      {/* Problem List */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {sampleProblems.map((problem) => (
          <div 
            key={problem.id} 
            className="bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6 hover:border-blue-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/10"
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-white mb-2">{problem.title}</h3>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-1 rounded text-xs ${
                    problem.difficulty === "Easy" ? "bg-green-500/20 text-green-400" :
                    problem.difficulty === "Medium" ? "bg-yellow-500/20 text-yellow-400" :
                    "bg-red-500/20 text-red-400"
                  }`}>
                    {problem.difficulty}
                  </span>
                  <span className="text-gray-400 text-sm">{problem.platform}</span>
                </div>
              </div>
            </div>
            
            <p className="text-gray-300 text-sm mb-6 line-clamp-3">
              {problem.description.split('\n')[0]}
            </p>
            
            <div className="flex items-center gap-3">
              <button
                onClick={() => openCodeEditor(problem)}
                className="flex-1 px-4 py-3 bg-gradient-to-r from-green-500 to-blue-500 hover:from-green-400 hover:to-blue-400 text-white rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
                Practice in CodeSpace
              </button>
              <a
                href={problem.url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition-colors"
              >
                Open in {problem.platform}
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* Coming Soon */}
      <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 border border-purple-500/20 rounded-2xl p-8 text-center">
        <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
          <span className="text-3xl">🚧</span>
        </div>
        <h3 className="text-xl font-bold text-white mb-2">More Problems Coming Soon!</h3>
        <p className="text-gray-400">
          We're working on integrating more problems from DSA CodeRush patterns.
          <br />Soon you'll be able to practice all 25 patterns directly in CodeSpace!
        </p>
      </div>
    </div>
  );
}

function DSACodeRush() {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedPattern, setSelectedPattern] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchDSAPatterns();
  }, []);

  const fetchDSAPatterns = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/api/stats/dsa-patterns"
      );
      const data = await response.json();
      setPatterns(data.patterns || []);
    } catch (error) {
      console.error("Error fetching DSA patterns:", error);
    } finally {
      setLoading(false);
    }
  };

  const openPattern = (pattern) => {
    setSelectedPattern(pattern);
    setShowModal(true);
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      Beginner: "text-green-400 bg-green-400/10 border-green-400/20",
      Intermediate: "text-yellow-400 bg-yellow-400/10 border-yellow-400/20",
      Advanced: "text-orange-400 bg-orange-400/10 border-orange-400/20",
      Expert: "text-red-400 bg-red-400/10 border-red-400/20",
    };
    return (
      colors[difficulty] || "text-gray-400 bg-gray-400/10 border-gray-400/20"
    );
  };

  return (
    <div className="mt-8">
      {/* Modern Header */}
      <div className="bg-gradient-to-r from-indigo-900/20 via-purple-900/20 to-pink-900/20 border border-indigo-500/20 rounded-2xl p-8 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center shadow-lg">
              <span className="text-3xl">🚀</span>
            </div>
            <div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-white via-indigo-200 to-purple-200 bg-clip-text text-transparent mb-2">
                DSA CodeRush
              </h2>
              <p className="text-indigo-200/80 text-lg">
                Master 25 essential patterns • Systematic approach •
                Expert-curated content
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-white">
              {patterns.length}
            </div>
            <div className="text-indigo-200/60 text-sm">Patterns Available</div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-12">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="ml-3 text-gray-400">Loading DSA patterns...</span>
        </div>
      ) : (
        <>
          {/* Pattern Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {patterns.map((pattern, idx) => (
              <div
                key={pattern.id}
                onClick={() => openPattern(pattern)}
                className="group relative bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-5 hover:border-indigo-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-indigo-500/10 cursor-pointer hover:-translate-y-1"
              >
                {/* Day Badge */}
                <div className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white text-sm font-bold shadow-lg">
                  {pattern.day}
                </div>

                {/* Pattern Icon & Title */}
                <div className="flex items-center gap-3 mb-4">
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-lg"
                    style={{
                      backgroundColor: pattern.color + "20",
                      border: `2px solid ${pattern.color}30`,
                    }}
                  >
                    {pattern.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-white font-semibold text-lg leading-tight">
                      {pattern.title}
                    </h3>
                  </div>
                </div>

                {/* Difficulty Badge */}
                <div
                  className={`inline-flex items-center gap-1 px-2 py-1 rounded-lg border text-sm font-medium mb-4 ${getDifficultyColor(
                    pattern.difficulty
                  )}`}
                >
                  <div className="w-2 h-2 rounded-full bg-current"></div>
                  {pattern.difficulty}
                </div>

                {/* Learn Button */}
                <button className="w-full px-4 py-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 hover:from-indigo-500/30 hover:to-purple-500/30 border border-indigo-500/30 hover:border-indigo-400/50 text-indigo-300 hover:text-white rounded-xl font-medium transition-all duration-200 flex items-center justify-center gap-2 group-hover:shadow-lg">
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                    />
                  </svg>
                  Learn Pattern
                </button>
              </div>
            ))}
          </div>

          {/* Progress Summary */}
          <div className="mt-8 bg-gradient-to-r from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-lg font-semibold text-white mb-1">
                  Learning Progress
                </h3>
                <p className="text-gray-400 text-sm">
                  Master these patterns to excel in coding interviews
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-indigo-400">
                  0/{patterns.length}
                </div>
                <div className="text-gray-400 text-sm">Completed</div>
              </div>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full"
                style={{ width: "0%" }}
              ></div>
            </div>
          </div>
        </>
      )}

      {/* Pattern Detail Modal */}
      {showModal && selectedPattern && (
        <PatternModal
          pattern={selectedPattern}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
}

function PatternModal({ pattern, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-gradient-to-br from-gray-900/95 via-gray-800/95 to-gray-900/95 border border-gray-700/50 rounded-3xl shadow-2xl overflow-hidden backdrop-blur-md">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-900/30 via-purple-900/30 to-pink-900/30 border-b border-indigo-500/20 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div
                className="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl shadow-lg"
                style={{
                  backgroundColor: pattern.color + "30",
                  border: `2px solid ${pattern.color}50`,
                }}
              >
                {pattern.icon}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white mb-1">
                  Day {pattern.day}: {pattern.title}
                </h2>
                <p className="text-indigo-200/70">
                  Essential DSA Pattern for Coding Success
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-3 rounded-xl hover:bg-white/10 text-gray-300 hover:text-white transition-all duration-200"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6">
          <div className="bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-2xl p-6 mb-6">
            <h3 className="text-lg font-semibold text-white mb-4">
              📄 PDF Content
            </h3>
            <div className="text-gray-300 bg-black/20 rounded-xl p-4 border border-white/10">
              <p className="text-center text-gray-400 py-8">
                📋 PDF content will be displayed here once extracted from:
                <br />
                <span className="font-mono text-indigo-300">
                  {pattern.title}.pdf
                </span>
                <br />
                <br />
                <span className="text-sm">
                  Please extract the text content from the PDF files in the DSA
                  Patterns folder and replace this placeholder with the actual
                  learning material.
                </span>
              </p>
            </div>
          </div>

          {/* Practice Problems Section */}
          <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6">
            <h3 className="text-lg font-semibold text-white mb-4">
              🎯 Practice Problems
            </h3>
            <div className="grid gap-4">
              {pattern.problems && pattern.problems.length > 0 ? (
                pattern.problems.map((problem, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-4 bg-black/20 rounded-xl border border-white/10"
                  >
                    <div>
                      <div className="text-white font-medium">
                        {problem.title}
                      </div>
                      <div className="text-sm text-gray-400">
                        {problem.difficulty}
                      </div>
                    </div>
                    <a
                      href={problem.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-400 hover:to-purple-400 text-white rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-indigo-500/25"
                    >
                      Solve
                    </a>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-400 py-8">
                  Practice problems will be added based on the pattern content
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SettingsPanel({
  onClose,
  accounts,
  setAccounts,
  prefs,
  setPrefs,
  onSave,
  saving,
  onSaveProfile,
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
      />
      <div className="relative w-full max-w-2xl max-h-[90vh] bg-gradient-to-br from-gray-900/95 via-gray-800/95 to-gray-900/95 border border-gray-700/50 rounded-3xl shadow-2xl overflow-hidden backdrop-blur-md">
        {/* Header with Gradient */}
        <div className="bg-gradient-to-r from-purple-900/30 via-blue-900/30 to-cyan-900/30 border-b border-purple-500/20 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center shadow-lg">
                <svg
                  className="w-7 h-7 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </div>
              <div>
                <h2 className="text-2xl font-bold bg-gradient-to-r from-white to-purple-200 bg-clip-text text-transparent">
                  Settings
                </h2>
                <p className="text-purple-200/70 text-sm">
                  Customize your CodeJarvis experience
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-3 rounded-xl hover:bg-white/10 text-gray-300 hover:text-white transition-all duration-200 group"
              title="Close Settings"
            >
              <svg
                className="w-6 h-6 group-hover:rotate-90 transition-transform duration-200"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Scrollable Content */}
        <div className="overflow-y-auto max-h-[calc(90vh-120px)] p-6 space-y-8">
          {/* Profile Section */}
          <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">
                  Profile Settings
                </h3>
                <p className="text-gray-400 text-sm">
                  Manage your personal information
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Profile Picture
                </label>
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white text-lg font-bold border-2 border-white/20">
                    {prefs.avatar ? (
                      <img
                        src={prefs.avatar}
                        alt="Profile"
                        className="w-full h-full rounded-2xl object-cover"
                      />
                    ) : (
                      "??"
                    )}
                  </div>
                  <div className="flex-1">
                    <input
                      type="file"
                      accept="image/*"
                      id="avatar-upload"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files && e.target.files[0];
                        if (!file) return;
                        const reader = new FileReader();
                        reader.onload = () => {
                          const dataUrl = reader.result;
                          setPrefs((p) => ({ ...p, avatar: dataUrl }));
                        };
                        reader.readAsDataURL(file);
                      }}
                    />
                    <label
                      htmlFor="avatar-upload"
                      className="cursor-pointer inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-400 hover:to-blue-400 text-white rounded-xl font-medium transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                        />
                      </svg>
                      Upload Image
                    </label>
                    <p className="text-xs text-gray-400 mt-2">
                      JPG, PNG or GIF (max 2MB)
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={onSaveProfile}
                className="w-full px-4 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-emerald-500/25"
              >
                Save Profile Changes
              </button>
            </div>
          </div>

          {/* Platform Connections */}
          <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">
                  Platform Connections
                </h3>
                <p className="text-gray-400 text-sm">
                  Link your coding platform accounts
                </p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <ModernTextField
                label="Codeforces"
                value={accounts.codeforces}
                onChange={(v) => setAccounts({ ...accounts, codeforces: v })}
                placeholder="Enter username"
                icon="CF"
                color="#1F8ACB"
              />
              <ModernTextField
                label="LeetCode"
                value={accounts.leetcode}
                onChange={(v) => setAccounts({ ...accounts, leetcode: v })}
                placeholder="Enter username"
                icon="LC"
                color="#FFA116"
              />
              <ModernTextField
                label="AtCoder"
                value={accounts.atcoder}
                onChange={(v) => setAccounts({ ...accounts, atcoder: v })}
                placeholder="Enter username"
                icon="AC"
                color="#3F7FBF"
              />
              <ModernTextField
                label="CodeChef"
                value={accounts.codechef}
                onChange={(v) => setAccounts({ ...accounts, codechef: v })}
                placeholder="Enter username"
                icon="CC"
                color="#8B4513"
              />
            </div>

            <button
              onClick={onSave}
              disabled={saving}
              className="w-full mt-6 px-4 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-400 hover:to-cyan-400 disabled:from-gray-600 disabled:to-gray-700 text-white rounded-xl font-semibold transition-all duration-200 shadow-lg hover:shadow-blue-500/25 disabled:cursor-not-allowed disabled:shadow-none flex items-center justify-center gap-2"
            >
              {saving ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Saving Platforms...
                </>
              ) : (
                <>
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3-3m0 0l-3 3m3-3v12"
                    />
                  </svg>
                  Save Platform Connections
                </>
              )}
            </button>
          </div>

          {/* Preferences */}
          <div className="bg-gradient-to-br from-gray-800/40 to-gray-900/60 border border-gray-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl flex items-center justify-center">
                <svg
                  className="w-6 h-6 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-white">
                  Preferences
                </h3>
                <p className="text-gray-400 text-sm">
                  Customize your notification settings
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <ModernToggleField
                label="Email Reminders"
                description="Get notified about upcoming contests"
                checked={prefs.emailReminders}
                onChange={(v) => setPrefs({ ...prefs, emailReminders: v })}
                icon="📧"
              />
              <ModernToggleField
                label="Product Updates"
                description="Receive news about CodeJarvis features"
                checked={prefs.newsletter}
                onChange={(v) => setPrefs({ ...prefs, newsletter: v })}
                icon="📰"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ModernTextField({ label, value, onChange, placeholder, icon, color }) {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-300">{label}</label>
      <div className="relative">
        <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center gap-2">
          <div
            className="w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold text-white"
            style={{
              backgroundColor: color + "40",
              border: `1px solid ${color}30`,
            }}
          >
            {icon}
          </div>
        </div>
        <input
          className="w-full pl-12 pr-4 py-3 rounded-xl bg-black/40 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-200 backdrop-blur-sm"
          value={value || ""}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
        />
      </div>
    </div>
  );
}

function ModernToggleField({ label, description, checked, onChange, icon }) {
  return (
    <div className="flex items-center justify-between p-4 rounded-xl bg-black/20 border border-white/10 hover:border-white/20 transition-all duration-200">
      <div className="flex items-center gap-3">
        <div className="text-2xl">{icon}</div>
        <div>
          <div className="text-white font-medium">{label}</div>
          <div className="text-gray-400 text-sm">{description}</div>
        </div>
      </div>
      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`relative w-14 h-8 rounded-full transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-purple-500/50 ${
          checked
            ? "bg-gradient-to-r from-emerald-500 to-teal-500 shadow-lg shadow-emerald-500/25"
            : "bg-gray-600"
        }`}
      >
        <span
          className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform duration-300 shadow-md ${
            checked ? "translate-x-6" : "translate-x-0"
          }`}
        />
      </button>
    </div>
  );
}

function ToggleField({ label, checked, onChange }) {
  return (
    <label className="flex items-center justify-between bg-gray-800 border border-gray-700 rounded px-3 py-2">
      <span className="text-gray-300">{label}</span>
      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`w-10 h-6 rounded-full relative transition-colors ${
          checked ? "bg-emerald-600" : "bg-gray-700"
        }`}
      >
        <span
          className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full transition-transform ${
            checked ? "translate-x-4" : ""
          }`}
        />
      </button>
    </label>
  );
}
