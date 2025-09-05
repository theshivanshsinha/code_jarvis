import { useState } from "react";

export default function Landing() {
  const [showContests, setShowContests] = useState(false);

  const startWithGoogle = () => {
    window.location.href = "http://localhost:5000/api/auth/google/url";
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xl font-bold">
          <svg className="w-6 h-6 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 4h18v4a6 6 0 0 1-6 6H9a6 6 0 0 1-6-6V4z"/>
            <path d="M7 20h10"/>
            <path d="M12 14v6"/>
          </svg>
          ContestHub
        </div>
        <nav className="space-x-4 text-sm">
          <a className="hover:text-blue-300" href="#features">Features</a>
        </nav>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">
            Grow your coding career, not just your rating
          </h1>
          <p className="text-gray-300 mt-4">
            Track contests from Codeforces, LeetCode, AtCoder and more — and go beyond.
            Understand your strengths and weaknesses by topic and difficulty, get a personalized
            roadmap, and build consistent habits that move your career forward.
          </p>
          <div className="mt-8 flex gap-4">
            <button onClick={startWithGoogle} className="group inline-flex items-center gap-2 px-5 py-3 bg-blue-600 hover:bg-blue-500 rounded font-semibold transition-transform duration-150 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-500/40">
              <svg className="w-5 h-5 text-white/90 transition-transform duration-150 group-hover:-translate-y-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21.35 11.1H12v2.9h5.35A5.9 5.9 0 1 1 12 6.1c1.43 0 2.73.51 3.75 1.36l1.98-2.22A8.96 8.96 0 0 0 12 3.1a9 9 0 1 0 9 9c0-.33-.02-.66-.05-.99z"/>
              </svg>
              Get Started
            </button>
            <button onClick={() => setShowContests((s) => !s)} className="group inline-flex items-center gap-2 px-5 py-3 bg-gray-800 hover:bg-gray-700 rounded transition-transform duration-150 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-gray-500/30">
              <svg className="w-5 h-5 text-blue-300 transition-transform duration-150 group-hover:translate-x-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2"/>
                <path d="M16 2v4M8 2v4M3 10h18"/>
              </svg>
              View Upcoming Contests
            </button>
          </div>
        </div>
        <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
          <ul className="space-y-3">
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-blue-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 12h18"/><path d="M3 6h18"/><path d="M3 18h18"/>
              </svg>
              <span>Unified contest feed</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-emerald-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/>
              </svg>
              <span>One‑click registration & reminders</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-purple-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>
              </svg>
              <span>Cross‑platform stats (CF, LC, AtCoder…)</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-amber-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 20h18"/><path d="M8 20V10l4-3 4 3v10"/>
              </svg>
              <span>Topic mastery: strengths & weak areas</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-sky-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 12h7l2-3 2 3h7"/>
              </svg>
              <span>Personalized practice roadmap</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-rose-400 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M3 8h4v8H3zM10 4h4v16h-4zM17 10h4v6h-4z"/>
              </svg>
              <span>Streaks and smart goals</span>
            </li>
          </ul>
        </div>
      </main>
      <section className="max-w-6xl mx-auto px-6 pb-16 grid md:grid-cols-3 gap-6">
        <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-2 text-xl font-semibold mb-2">
            <svg className="w-5 h-5 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2l3 7 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z"/>
            </svg>
            Know your strengths
          </div>
          <p className="text-gray-300 text-sm">
            Automatic analysis across topics like DP, graphs, greedy, math, and more. See what you
            consistently solve fast and where you spike.
          </p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-2 text-xl font-semibold mb-2">
            <svg className="w-5 h-5 text-amber-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            </svg>
            Fix your gaps
          </div>
          <p className="text-gray-300 text-sm">
            Identify weak topics and drill with curated sets that adapt as you improve. Track accuracy,
            speed, and difficulty progression over time.
          </p>
        </div>
        <div className="bg-gray-800/60 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-2 text-xl font-semibold mb-2">
            <svg className="w-5 h-5 text-sky-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M3 6h18M3 12h10M3 18h6"/>
            </svg>
            Follow your roadmap
          </div>
          <p className="text-gray-300 text-sm">
            A weekly plan balancing practice, contests, and reviews. Stay on track with reminders,
            streaks, and gentle nudges when you slip.
          </p>
        </div>
      </section>
      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="bg-gray-800/40 border border-gray-700 rounded-xl p-6 md:p-8">
          <div className="text-2xl font-bold">How it works</div>
          <ol className="mt-4 grid md:grid-cols-3 gap-4 text-sm text-gray-300">
            <li className="bg-gray-800/40 border border-gray-700 rounded p-4">
              <div className="flex items-center gap-2 font-semibold mb-1">
                <svg className="w-4 h-4 text-blue-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
                1. Sign in with Google
              </div>
              Pull your contest data and set your goals.
            </li>
            <li className="bg-gray-800/40 border border-gray-700 rounded p-4">
              <div className="flex items-center gap-2 font-semibold mb-1">
                <svg className="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 12l6 6L21 6"/>
                </svg>
                2. Get your insights
              </div>
              See topic‑wise strengths, weak areas, and trend lines.
            </li>
            <li className="bg-gray-800/40 border border-gray-700 rounded p-4">
              <div className="flex items-center gap-2 font-semibold mb-1">
                <svg className="w-4 h-4 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M3 3h18v4H3zM7 7v14"/><path d="M11 11h8M11 15h6M11 19h4"/>
                </svg>
                3. Follow the roadmap
              </div>
              Practice sets, contest schedule, and reminders—automated.
            </li>
          </ol>
        </div>
      </section>
      {showContests && <LandingContests />}
    </div>
  )
}

function LandingContests() {
  const [contests, setContests] = useState([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/api/contests");
      const data = await res.json();
      setContests(data);
    } catch (e) {
      setContests([]);
    } finally {
      setLoading(false);
    }
  };

  useState(() => { load(); }, []);

  return (
    <div className="max-w-6xl mx-auto px-6 pb-16">
      <h2 className="text-2xl font-bold mb-4">Upcoming Contests</h2>
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
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


