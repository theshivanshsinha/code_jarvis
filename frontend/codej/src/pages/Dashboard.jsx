import { useEffect, useState } from "react";

export default function Dashboard() {
  const [contests, setContests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/contests")
      .then((r) => r.json())
      .then((data) => setContests(data))
      .finally(() => setLoading(false));
    fetch("http://localhost:5000/api/stats")
      .then((r) => r.json())
      .then(setStats);
  }, []);

  const remind = async (contest) => {
    try {
      const res = await fetch("http://localhost:5000/api/reminders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: `${contest.platform}: ${contest.name}`,
          start: contest.start,
          url: contest.url,
        }),
      });
      if (!res.ok) throw new Error("Failed");
      setMessage("Reminder created!");
      setTimeout(() => setMessage(""), 2000);
    } catch (e) {
      setMessage("Failed to create reminder");
      setTimeout(() => setMessage(""), 2000);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-5xl mx-auto px-6 py-8">
        <h1 className="text-3xl font-bold mb-6">Upcoming Contests</h1>
        {message && <div className="mb-4 text-green-400">{message}</div>}
        {stats && (
          <div className="mb-6 bg-gray-800 border border-gray-700 rounded p-4">
            <div className="text-xl font-semibold mb-2">Your Stats</div>
            <div className="text-sm text-gray-300">Total Contests: {stats.totalContests}</div>
            <div className="text-sm text-gray-300">Max Rating: {stats.maxRating.platform} {stats.maxRating.value}</div>
            <div className="text-sm text-gray-300">Solved: LC {stats.problemSolved.leetcode}, CF {stats.problemSolved.codeforces}</div>
          </div>
        )}
        {loading ? (
          <div>Loading…</div>
        ) : (
          <div className="grid sm:grid-cols-2 gap-4">
            {contests.map((c, idx) => (
              <div key={idx} className="bg-gray-800 border border-gray-700 rounded p-4">
                <div className="text-sm text-blue-300">{c.platform}</div>
                <div className="text-lg font-semibold">{c.name}</div>
                <div className="text-sm text-gray-300 mt-1">Starts: {new Date(c.start).toLocaleString()}</div>
                <div className="text-sm text-gray-300">Duration: {c.durationMinutes} min</div>
                <div className="mt-3 flex gap-3">
                  <a href={c.url} target="_blank" rel="noreferrer" className="px-3 py-1 rounded bg-blue-600 hover:bg-blue-500">Register</a>
                  <button onClick={() => remind(c)} className="px-3 py-1 rounded bg-gray-700 hover:bg-gray-600">Remind me</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}


