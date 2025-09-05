import React, { useState, useEffect } from "react";

function SimpleCalendar({ userEmail }) {
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (userEmail) {
      fetchCalendarEvents();
    }
  }, [userEmail]);

  const fetchCalendarEvents = async () => {
    try {
      setLoading(true);
      const response = await fetch(
        "http://localhost:5000/api/reminders/calendar"
      );
      const data = await response.json();

      if (data.success) {
        // Filter events for current user
        const userEvents = data.events.filter(
          (event) => event.user_email === userEmail
        );
        setCalendarEvents(userEvents);
      } else {
        setError("Failed to load calendar events");
      }
    } catch (err) {
      setError("Error fetching calendar events");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return dateStr;
    }
  };

  const getTimeUntil = (dateStr) => {
    try {
      const now = new Date();
      const eventDate = new Date(dateStr);
      const diffMs = eventDate - now;

      if (diffMs <= 0) {
        return "Started";
      }

      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      const diffHours = Math.floor(
        (diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );
      const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

      if (diffDays > 0) {
        return `${diffDays}d ${diffHours}h`;
      } else if (diffHours > 0) {
        return `${diffHours}h ${diffMinutes}m`;
      } else {
        return `${diffMinutes}m`;
      }
    } catch {
      return "Soon";
    }
  };

  const getPlatformColor = (platform) => {
    const colors = {
      leetcode: "#FFA116",
      codeforces: "#1F8ACB",
      atcoder: "#3F7FBF",
      codechef: "#5B4638",
      unknown: "#6B7280",
    };
    return colors[platform?.toLowerCase()] || colors.unknown;
  };

  const generateCalendarDays = () => {
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();

    // Get first day of month and number of days
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const startingDayOfWeek = firstDay.getDay(); // 0 = Sunday
    const daysInMonth = lastDay.getDate();

    // Create array of days
    const days = [];

    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }

    // Add all days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day);
      const dateStr = date.toISOString().split("T")[0];

      // Find events for this day
      const dayEvents = calendarEvents.filter((event) => {
        const eventDate = new Date(event.start);
        return eventDate.toDateString() === date.toDateString();
      });

      days.push({
        date: day,
        dateStr,
        isToday: date.toDateString() === now.toDateString(),
        events: dayEvents,
      });
    }

    return {
      days,
      monthName: firstDay.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      }),
    };
  };

  const getEventTimeOnly = (dateStr) => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      });
    } catch {
      return "";
    }
  };

  if (loading) {
    return (
      <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3 text-white">
          Contest Calendar
        </h3>
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-gray-400">Loading calendar...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-3 text-white">
          Contest Calendar
        </h3>
        <div className="text-center py-6">
          <p className="text-red-400 mb-2">Error loading calendar</p>
          <p className="text-gray-500 text-sm">{error}</p>
          <button
            onClick={fetchCalendarEvents}
            className="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { days, monthName } = generateCalendarDays();
  const weekDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  return (
    <div className="bg-gray-800/60 border border-gray-700 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Contest Calendar</h3>
        <button
          onClick={fetchCalendarEvents}
          className="p-2 text-gray-400 hover:text-white transition-colors"
          title="Refresh calendar"
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
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
        </button>
      </div>

      {calendarEvents.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📅</div>
          <p className="text-gray-400 mb-2">No upcoming contests</p>
          <p className="text-sm text-gray-500">
            Set reminders for contests to see them here!
          </p>
        </div>
      ) : (
        <div className="calendar-container">
          {/* Month Header */}
          <div className="text-center mb-4">
            <h4 className="text-white font-semibold text-lg">{monthName}</h4>
          </div>

          {/* Day Headers */}
          <div className="grid grid-cols-7 gap-1 mb-2">
            {weekDays.map((day) => (
              <div
                key={day}
                className="text-center text-gray-400 text-sm font-medium py-2"
              >
                {day}
              </div>
            ))}
          </div>

          {/* Calendar Grid */}
          <div className="grid grid-cols-7 gap-1">
            {days.map((dayData, index) => {
              if (!dayData) {
                // Empty cell for days before month starts
                return <div key={index} className="h-20"></div>;
              }

              return (
                <div
                  key={index}
                  className={`
                    h-20 border border-gray-700 rounded p-1 relative overflow-hidden
                    ${
                      dayData.isToday
                        ? "bg-blue-900/30 border-blue-500"
                        : "bg-gray-800/30"
                    }
                    ${dayData.events.length > 0 ? "hover:bg-gray-700/50" : ""}
                    transition-colors
                  `}
                >
                  {/* Day Number */}
                  <div
                    className={`text-xs font-medium ${
                      dayData.isToday ? "text-blue-300" : "text-gray-300"
                    }`}
                  >
                    {dayData.date}
                  </div>

                  {/* Events */}
                  <div className="mt-1 space-y-1">
                    {dayData.events.slice(0, 2).map((event, eventIdx) => (
                      <div
                        key={eventIdx}
                        className="text-xs px-1 py-0.5 rounded truncate"
                        style={{
                          backgroundColor: `${getPlatformColor(
                            event.platform
                          )}30`,
                          color: getPlatformColor(event.platform),
                          fontSize: "10px",
                        }}
                        title={`${event.title} - ${getEventTimeOnly(
                          event.start
                        )}`}
                      >
                        <div className="flex items-center gap-1">
                          <div
                            className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                            style={{
                              backgroundColor: getPlatformColor(event.platform),
                            }}
                          ></div>
                          <span className="truncate">
                            {event.title.slice(0, 15)}
                          </span>
                        </div>
                        <div
                          className="text-gray-400"
                          style={{ fontSize: "9px" }}
                        >
                          {getEventTimeOnly(event.start)}
                        </div>
                      </div>
                    ))}

                    {/* Show +more indicator if more than 2 events */}
                    {dayData.events.length > 2 && (
                      <div
                        className="text-xs text-gray-400"
                        style={{ fontSize: "9px" }}
                      >
                        +{dayData.events.length - 2} more
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Legend */}
          <div className="mt-4 flex flex-wrap gap-3 text-xs">
            {[...new Set(calendarEvents.map((e) => e.platform))].map(
              (platform) => (
                <div key={platform} className="flex items-center gap-1">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ backgroundColor: getPlatformColor(platform) }}
                  ></div>
                  <span className="text-gray-400 capitalize">{platform}</span>
                </div>
              )
            )}
          </div>
        </div>
      )}

      {calendarEvents.length > 0 && (
        <div className="mt-4 pt-3 border-t border-gray-700">
          <p className="text-xs text-gray-500 text-center">
            {calendarEvents.length} active reminder
            {calendarEvents.length !== 1 ? "s" : ""}
          </p>
        </div>
      )}
    </div>
  );
}

export default SimpleCalendar;
