import { useEffect, useState } from "react";

export default function Accounts() {
  const [accounts, setAccounts] = useState({ codeforces: "", leetcode: "", atcoder: "", codechef: "" });
  const [notice, setNotice] = useState("");

  const connectGoogle = async () => {
    const res = await fetch("http://localhost:5000/api/auth/google/url");
    const data = await res.json();
    window.location.href = data.url;
  };

  const save = async () => {
    const token = localStorage.getItem("session_token") || "";
    const res = await fetch("http://localhost:5000/api/accounts", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ accounts }),
    });
    setNotice(res.ok ? "Saved" : "Failed");
    setTimeout(() => setNotice(""), 1500);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-3xl mx-auto px-6 py-12 space-y-6">
        <h1 className="text-3xl font-bold">Connected Accounts</h1>
        <p className="text-gray-300">Connect Google to enable Calendar reminders and easy sign-in.</p>
        <button onClick={connectGoogle} className="px-4 py-2 rounded bg-blue-600 hover:bg-blue-500">Connect Google</button>

        <div className="bg-gray-800 border border-gray-700 rounded p-6 space-y-4">
          <h2 className="text-xl font-semibold">Coding Platform Usernames</h2>
          <div className="grid sm:grid-cols-2 gap-4">
            <input value={accounts.codeforces} onChange={(e)=>setAccounts({...accounts, codeforces: e.target.value})} placeholder="Codeforces handle" className="bg-gray-900 border border-gray-700 rounded px-3 py-2" />
            <input value={accounts.leetcode} onChange={(e)=>setAccounts({...accounts, leetcode: e.target.value})} placeholder="LeetCode username" className="bg-gray-900 border border-gray-700 rounded px-3 py-2" />
            <input value={accounts.atcoder} onChange={(e)=>setAccounts({...accounts, atcoder: e.target.value})} placeholder="AtCoder username" className="bg-gray-900 border border-gray-700 rounded px-3 py-2" />
            <input value={accounts.codechef} onChange={(e)=>setAccounts({...accounts, codechef: e.target.value})} placeholder="CodeChef username" className="bg-gray-900 border border-gray-700 rounded px-3 py-2" />
          </div>
          <button onClick={save} className="px-4 py-2 rounded bg-green-600 hover:bg-green-500">Save</button>
          {notice && <div className="text-sm text-blue-300">{notice}</div>}
        </div>
      </div>
    </div>
  );
}


