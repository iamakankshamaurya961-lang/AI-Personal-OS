/* =========================================================
   AI PERSONAL OS — FRONTEND JAVASCRIPT
   ========================================================= */

const API = "http://127.0.0.1:8000";

let currentEmailBody = "";
let currentEmailId = null;

const main = document.querySelector(".main");


/* =========================================================
   HELPERS
   ========================================================= */

function escapeHtml(value) {
    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


async function fetchJSON(url, options = {}) {
    const response = await fetch(url, options);

    let data = {};

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (!response.ok) {
        throw new Error(
            data.error ||
            data.message ||
            `Request failed: ${response.status}`
        );
    }

    return data;
}


/* =========================================================
   DASHBOARD
   ========================================================= */

async function showDashboard() {

    main.innerHTML = `
        <div class="card loading-card">
            <div class="loading-icon">🤖</div>
            <h2>Loading AI Personal OS...</h2>
            <p>Preparing your dashboard...</p>
        </div>
    `;

    try {

        const [
            assignments,
            timetable,
            tasks,
            events,
            memoryData
        ] = await Promise.all([
            fetchJSON(`${API}/assignments`),
            fetchJSON(`${API}/timetable`),
            fetchJSON(`${API}/tasks`),
            fetchJSON(`${API}/calendar`),
            fetchJSON(`${API}/memory`)
        ]);


        const pendingAssignments =
            assignments.filter(
                item => item.status !== "completed"
            ).length;


        const pendingTasks =
            tasks.filter(
                item => item.status !== "completed"
            ).length;


        const memoryCount =
            Array.isArray(memoryData.memory)
                ? memoryData.memory.length
                : 0;


        const nextAssignment =
            assignments.length
                ? assignments[0]
                : null;


        const nextClass =
            timetable.length
                ? timetable[0]
                : null;


        const nextEvent =
            events.length
                ? events[0]
                : null;


        main.innerHTML = `

            <div class="dashboard-container">

                <!-- HEADER -->

                <div class="dashboard-header">

                    <div>

                        <h1 id="greeting">
                            👋 Welcome, Akanksha Maurya
                        </h1>

                        <p class="dashboard-subtitle">
                            Your AI-powered Personal Operating System
                        </p>

                        <p id="current-date"></p>

                        <p id="current-time"></p>

                    </div>


                    <div class="dashboard-search">

                        <input
                            type="text"
                            id="globalSearch"
                            class="search-box"
                            placeholder="🔍 Search Assignments, Events, Classes..."
                            autocomplete="off"
                        >

                        <div id="searchResults"></div>

                    </div>

                </div>


                <!-- QUICK ACTIONS -->

                <div class="quick-grid">

                    <div class="quick-card">

                        <div class="quick-icon">💬</div>

                        <h2>AI Assistant</h2>

                        <p>
                            Chat with your AI assistant.
                        </p>

                        <button onclick="showChat()">
                            Open Chat
                        </button>

                    </div>


                    <div class="quick-card">

                        <div class="quick-icon">📄</div>

                        <h2>Documents</h2>

                        <p>
                            Upload and chat with PDFs.
                        </p>

                        <button onclick="showDocuments()">
                            Upload PDF
                        </button>

                    </div>


                    <div class="quick-card">

                        <div class="quick-icon">📚</div>

                        <h2>Assignments</h2>

                        <p>
                            Manage your assignments.
                        </p>

                        <button onclick="showAssignments()">
                            Open
                        </button>

                    </div>


                    <div class="quick-card">

                        <div class="quick-icon">✅</div>

                        <h2>Tasks</h2>

                        <p>
                            Track your daily tasks.
                        </p>

                        <button onclick="showTasks()">
                            Open
                        </button>

                    </div>

                </div>


                <!-- STATISTICS -->

                <h2 class="section-title">
                    📊 Quick Statistics
                </h2>


                <div class="statistics-grid">

                    <div class="stat-card">

                        <div class="stat-title">
                            📚 Pending Assignments
                        </div>

                        <div class="stat-number">
                            ${pendingAssignments}
                        </div>

                    </div>


                    <div class="stat-card">

                        <div class="stat-title">
                            ✅ Pending Tasks
                        </div>

                        <div class="stat-number">
                            ${pendingTasks}
                        </div>

                    </div>


                    <div class="stat-card">

                        <div class="stat-title">
                            📅 Total Classes
                        </div>

                        <div class="stat-number">
                            ${timetable.length}
                        </div>

                    </div>


                    <div class="stat-card">

                        <div class="stat-title">
                            📅 Events
                        </div>

                        <div class="stat-number">
                            ${events.length}
                        </div>

                    </div>


                    <div class="stat-card">

                        <div class="stat-title">
                            🧠 Memories
                        </div>

                        <div class="stat-number">
                            ${memoryCount}
                        </div>

                    </div>

                </div>


                <!-- PROGRESS -->

                <div class="dashboard-large-card">

                    <h2>
                        📊 Overall Progress
                    </h2>

                    <p>
                        🚀 Your AI Personal OS is almost complete.
                    </p>

                    <div class="progress-bar">

                        <div
                            class="progress-fill"
                            style="width:92%;"
                        ></div>

                    </div>

                </div>


                <!-- PRODUCTIVITY -->

                <div class="dashboard-large-card">

                    <h2>
                        ⚡ Productivity Score
                    </h2>

                    <div class="productivity-score">
                        92%
                    </div>

                    <p>
                        Keep completing your tasks and assignments
                        to maintain your productivity.
                    </p>

                </div>


                <!-- RECENT ACTIVITY -->

                <div class="dashboard-large-card">

                    <h2>
                        📝 Recent Activity
                    </h2>

                    <ul class="activity-list">

                        <li>✅ Dashboard updated</li>

                        <li>📚 Assignments synced</li>

                        <li>📅 Calendar loaded</li>

                        <li>🤖 AI system connected</li>

                        <li>🔔 Notifications active</li>

                    </ul>

                </div>


                <!-- AI TIP -->

                <div class="dashboard-large-card">

                    <h2>
                        💡 AI Tip of the Day
                    </h2>

                    <p>
                        Complete today's assignments before
                        starting new tasks.
                    </p>

                </div>


                <!-- UPCOMING -->

                <h2 class="section-title">
                    📌 Upcoming Activities
                </h2>


                <div class="upcoming-grid">

                    <div class="upcoming-card">

                        <h2>
                            📚 Upcoming Assignment
                        </h2>

                        ${
                            nextAssignment
                                ? `
                                    <h3>
                                        ${escapeHtml(
                                            nextAssignment.title ||
                                            "Untitled Assignment"
                                        )}
                                    </h3>

                                    <p>
                                        📖 ${escapeHtml(
                                            nextAssignment.subject ||
                                            "No subject"
                                        )}
                                    </p>

                                    <p>
                                        📅 ${escapeHtml(
                                            nextAssignment.deadline ||
                                            "No deadline"
                                        )}
                                    </p>
                                `
                                : `
                                    <p>
                                        No upcoming assignments.
                                    </p>
                                `
                        }

                    </div>


                    <div class="upcoming-card">

                        <h2>
                            📅 Next Class
                        </h2>

                        ${
                            nextClass
                                ? `
                                    <h3>
                                        ${escapeHtml(
                                            nextClass.subject ||
                                            "Class"
                                        )}
                                    </h3>

                                    <p>
                                        ${escapeHtml(
                                            nextClass.day || ""
                                        )}
                                    </p>

                                    <p>
                                        🕒
                                        ${escapeHtml(
                                            nextClass.start_time || ""
                                        )}
                                        -
                                        ${escapeHtml(
                                            nextClass.end_time || ""
                                        )}
                                    </p>

                                    <p>
                                        📍
                                        ${escapeHtml(
                                            nextClass.location ||
                                            "No location"
                                        )}
                                    </p>
                                `
                                : `
                                    <p>
                                        No upcoming classes.
                                    </p>
                                `
                        }

                    </div>


                    <div class="upcoming-card">

                        <h2>
                            📅 Upcoming Event
                        </h2>

                        ${
                            nextEvent
                                ? `
                                    <h3>
                                        ${escapeHtml(
                                            nextEvent.event ||
                                            "Event"
                                        )}
                                    </h3>

                                    <p>
                                        📅
                                        ${escapeHtml(
                                            nextEvent.event_date ||
                                            ""
                                        )}
                                    </p>

                                    ${
                                        nextEvent.event_time
                                            ? `
                                                <p>
                                                    🕒
                                                    ${escapeHtml(
                                                        nextEvent.event_time
                                                    )}
                                                </p>
                                            `
                                            : ""
                                    }
                                `
                                : `
                                    <p>
                                        No upcoming events.
                                    </p>
                                `
                        }

                    </div>

                </div>

            </div>
        `;


        updateClock();
        setupSearch();

    } catch (error) {

        console.error(
            "Dashboard error:",
            error
        );


        main.innerHTML = `

            <div class="dashboard-large-card">

                <h2>
                    ⚠️ Dashboard Error
                </h2>

                <p>
                    Unable to load dashboard data.
                </p>

                <p>
                    ${escapeHtml(error.message)}
                </p>

                <button onclick="showDashboard()">
                    🔄 Retry
                </button>

            </div>
        `;
    }
}


/* =========================================================
   SEARCH
   ========================================================= */

function setupSearch() {

    const searchInput =
        document.getElementById("globalSearch");

    const searchResults =
        document.getElementById("searchResults");


    if (!searchInput || !searchResults) {
        return;
    }


    let searchTimeout;


    searchInput.addEventListener(
        "input",
        function () {

            clearTimeout(searchTimeout);

            const query =
                searchInput.value.trim();


            if (!query) {

                searchResults.innerHTML = "";

                searchResults.style.display =
                    "none";

                return;
            }


            searchResults.style.display =
                "block";


            searchResults.innerHTML = `
                <div class="search-loading">
                    🔎 Searching...
                </div>
            `;


            searchTimeout =
                setTimeout(
                    () => performSearch(query),
                    300
                );
        }
    );


    searchInput.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                searchInput.value = "";

                searchResults.innerHTML = "";

                searchResults.style.display =
                    "none";
            }
        }
    );
}


async function performSearch(query) {

    const searchResults =
        document.getElementById("searchResults");


    if (!searchResults) {
        return;
    }


    try {

        const results =
            await fetchJSON(
                `${API}/search?query=${encodeURIComponent(query)}`
            );


        if (!Array.isArray(results) || !results.length) {

            searchResults.innerHTML = `
                <div class="search-no-results">
                    🔍 No results found for
                    "<b>${escapeHtml(query)}</b>"
                </div>
            `;

            return;
        }


        searchResults.innerHTML = "";


        results.forEach(result => {

            const item =
                document.createElement("div");


            item.className =
                "search-result";


            item.innerHTML = `

                <div class="search-result-type">
                    ${escapeHtml(
                        result.type || "Result"
                    )}
                </div>

                <div class="search-result-title">
                    ${escapeHtml(
                        result.title || "Untitled"
                    )}
                </div>

                ${
                    result.subtitle
                        ? `
                            <div class="search-result-subtitle">
                                ${escapeHtml(
                                    result.subtitle
                                )}
                            </div>
                        `
                        : ""
                }
            `;


            item.addEventListener(
                "click",
                () => handleSearchResult(result)
            );


            searchResults.appendChild(item);

        });


        searchResults.style.display =
            "block";

    } catch (error) {

        console.error(
            "Search error:",
            error
        );


        searchResults.innerHTML = `
            <div class="search-error">
                ❌ Unable to connect to AI Personal OS.
            </div>
        `;
    }
}


function handleSearchResult(result) {

    const type =
        String(result.type || "").toLowerCase();


    const searchResults =
        document.getElementById("searchResults");


    if (searchResults) {
        searchResults.style.display = "none";
    }


    if (type.includes("assignment")) {
        showAssignments();

    } else if (type.includes("task")) {
        showTasks();

    } else if (
        type.includes("event") ||
        type.includes("calendar")
    ) {
        showCalendar();

    } else if (
        type.includes("class") ||
        type.includes("timetable")
    ) {
        showTimetable();
    }
}


/* =========================================================
   CHAT
   ========================================================= */

function showChat() {

    main.innerHTML = `

        <h1>
            💬 AI Chat
        </h1>

        <div class="chat-box">

            <div class="chat-toolbar">

                <button onclick="clearChat()">
                    🗑 Clear Chat
                </button>

            </div>

            <div id="chat-box"></div>

            <input
                id="question"
                type="text"
                placeholder="Ask anything..."
                autocomplete="off"
            >

            <div class="chat-actions">

                <button onclick="askAI()">
                    🤖 Ask AI
                </button>

                <button
                    id="voice-btn"
                    onclick="startVoice()"
                >
                    🎤 Speak
                </button>

            </div>

        </div>
    `;


    const input =
        document.getElementById("question");


    if (input) {

        input.addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {
                    askAI();
                }

            }
        );

        input.focus();
    }
}


async function clearChat() {

    try {

        await fetchJSON(
            `${API}/clear_chat`,
            {
                method: "DELETE"
            }
        );


        const chat =
            document.getElementById("chat-box");


        if (chat) {
            chat.innerHTML = "";
        }

    } catch (error) {

        console.error(error);

        alert("Unable to clear chat.");
    }
}


async function askAI() {

    const input =
        document.getElementById("question");


    if (!input) {
        return;
    }


    const question =
        input.value.trim();


    if (!question) {
        return;
    }


    const chat =
        document.getElementById("chat-box");


    if (!chat) {
        return;
    }


    chat.innerHTML += `

        <div class="user-message">

            <div class="avatar">
                👤
            </div>

            <div class="bubble">
                ${escapeHtml(question)}
            </div>

        </div>
    `;


    input.value = "";


    const thinking =
        document.createElement("div");


    thinking.className =
        "ai-thinking";


    thinking.textContent =
        "🤖 AI is thinking...";


    chat.appendChild(thinking);


    try {

        const data =
            await fetchJSON(
                `${API}/ask?question=${encodeURIComponent(question)}`
            );


        thinking.remove();


        chat.innerHTML += `

            <div class="ai-message">

                <div class="avatar">
                    🤖
                </div>

                <div class="bubble">

                    <div class="message-text"></div>

                    <div
                        class="feedback-buttons"
                        style="display:none;"
                    >

                        <button
                            onclick="copyMessage(this)"
                        >
                            📋 Copy
                        </button>

                        <button
                            onclick="speakMessage(this)"
                        >
                            🔊 Speak
                        </button>

                        <button
                            onclick="feedback(this,'like')"
                        >
                            👍
                        </button>

                        <button
                            onclick="feedback(this,'dislike')"
                        >
                            👎
                        </button>

                    </div>

                </div>

            </div>
        `;


        const messages =
            document.querySelectorAll(
                ".message-text"
            );


        const messageElement =
            messages[messages.length - 1];


        await typeMessage(
            messageElement,
            data.answer ||
            "No answer received."
        );


        const feedbackButtons =
            messageElement
                .closest(".bubble")
                .querySelector(
                    ".feedback-buttons"
                );


        if (feedbackButtons) {
            feedbackButtons.style.display =
                "flex";
        }


        chat.scrollTop =
            chat.scrollHeight;

    } catch (error) {

        thinking.remove();


        console.error(
            "AI error:",
            error
        );


        chat.innerHTML += `

            <div class="ai-message">

                <div class="avatar">
                    🤖
                </div>

                <div class="bubble">
                    ❌ Sorry, I couldn't connect
                    to the AI backend.
                </div>

            </div>
        `;
    }
}


async function typeMessage(element, text) {

    if (!element) {
        return;
    }


    const safeText =
        String(text || "");


    element.textContent = "";


    for (let i = 0; i < safeText.length; i++) {

        element.textContent +=
            safeText.charAt(i);

        await new Promise(
            resolve =>
                setTimeout(resolve, 10)
        );
    }
}


function copyMessage(button) {

    const bubble =
        button.closest(".bubble");


    const message =
        bubble?.querySelector(".message-text");


    if (!message) {
        return;
    }


    navigator.clipboard
        .writeText(message.innerText)
        .then(() => {

            button.textContent =
                "✅ Copied";

            setTimeout(
                () => {
                    button.textContent =
                        "📋 Copy";
                },
                1500
            );
        });
}


function feedback(button, type) {

    alert(
        type === "like"
            ? "Thanks for your feedback! 👍"
            : "Thanks! We'll improve the AI. 👎"
    );
}


function speakMessage(button) {

    const bubble =
        button.closest(".bubble");


    const message =
        bubble?.querySelector(".message-text");


    if (message) {
        speakText(message.innerText);
    }
}


function speakText(text) {

    if (!("speechSynthesis" in window)) {

        alert(
            "Speech synthesis is not supported."
        );

        return;
    }


    speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(text);


    speech.lang = "en-IN";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;


    speechSynthesis.speak(speech);
}


function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech Recognition is not supported in this browser."
        );

        return;
    }


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";

    recognition.interimResults =
        false;

    recognition.maxAlternatives =
        1;


    const button =
        document.getElementById("voice-btn");


    if (button) {
        button.textContent =
            "🎙 Listening...";
    }


    recognition.start();


    recognition.onresult =
        event => {

            const text =
                event.results[0][0]
                    .transcript;


            const question =
                document.getElementById(
                    "question"
                );


            if (question) {
                question.value = text;
            }


            if (button) {
                button.textContent =
                    "🎤 Speak";
            }


            askAI();
        };


    recognition.onerror =
        () => {

            if (button) {
                button.textContent =
                    "🎤 Speak";
            }
        };


    recognition.onend =
        () => {

            if (button) {
                button.textContent =
                    "🎤 Speak";
            }
        };
}


/* =========================================================
   DOCUMENTS
   ========================================================= */

function showDocuments() {

    main.innerHTML = `

        <h1>
            📄 Documents
        </h1>

        <div class="card">

            <h2>
                Upload Document
            </h2>

            <p>
                Upload a PDF to add it to your AI knowledge base.
            </p>

            <input
                type="file"
                id="pdfFile"
                accept=".pdf"
            >

            <br><br>

            <button onclick="uploadPDF()">
                📤 Upload PDF
            </button>

            <div id="upload-status"></div>

        </div>
    `;
}


async function uploadPDF() {

    const fileInput =
        document.getElementById("pdfFile");


    if (
        !fileInput ||
        !fileInput.files.length
    ) {

        alert("Please select a PDF.");

        return;
    }


    const formData =
        new FormData();


    formData.append(
        "file",
        fileInput.files[0]
    );


    const status =
        document.getElementById(
            "upload-status"
        );


    if (status) {
        status.textContent =
            "📤 Uploading...";
    }


    try {

        const response =
            await fetch(
                `${API}/upload`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const data =
            await response.json();


        if (!response.ok) {
            throw new Error(
                data.error ||
                data.message ||
                "Upload failed"
            );
        }


        if (status) {

            status.textContent =
                `✅ ${
                    data.message ||
                    "PDF uploaded successfully!"
                }`;
        }

    } catch (error) {

        console.error(
            "Upload error:",
            error
        );


        if (status) {

            status.textContent =
                `❌ ${error.message}`;
        }
    }
}


/* =========================================================
   MEMORY
   ========================================================= */

async function showMemory() {

    try {

        const data =
            await fetchJSON(
                `${API}/memory`
            );


        const memories =
            Array.isArray(data.memory)
                ? data.memory
                : [];


        main.innerHTML = `

            <h1>
                🧠 Memory
            </h1>

            <div class="card">

                <h2>
                    Saved Memories
                </h2>

                ${
                    memories.length
                        ? `
                            <ul class="memory-list">

                                ${
                                    memories
                                        .map(
                                            item => `
                                                <li>
                                                    ${escapeHtml(item)}
                                                </li>
                                            `
                                        )
                                        .join("")
                                }

                            </ul>
                        `
                        : `
                            <div class="empty-state">
                                🧠 No memories saved yet.
                            </div>
                        `
                }

            </div>
        `;

    } catch (error) {

        console.error(error);


        main.innerHTML = `

            <div class="card">

                <h2>
                    ❌ Failed to load memory
                </h2>

                <p>
                    ${escapeHtml(error.message)}
                </p>

            </div>
        `;
    }
}


/* =========================================================
   PROFILE
   ========================================================= */

async function showProfile() {

    try {

        const data =
            await fetchJSON(
                `${API}/profile`
            );


        main.innerHTML = `

            <h1>
                👤 Profile
            </h1>

            <div class="card profile-card">

                <label>Name</label>

                <input
                    id="name"
                    value="${escapeHtml(data.name)}"
                >


                <label>Email</label>

                <input
                    id="email"
                    value="${escapeHtml(data.email)}"
                >


                <label>Phone</label>

                <input
                    id="phone"
                    value="${escapeHtml(data.phone)}"
                >


                <label>College</label>

                <input
                    id="college"
                    value="${escapeHtml(data.college)}"
                >


                <label>Course</label>

                <input
                    id="course"
                    value="${escapeHtml(data.course)}"
                >


                <label>Semester</label>

                <input
                    id="semester"
                    value="${escapeHtml(data.semester)}"
                >


                <label>City</label>

                <input
                    id="city"
                    value="${escapeHtml(data.city)}"
                >


                <label>Goals</label>

                <textarea id="goals">${escapeHtml(
                    data.goals
                )}</textarea>


                <button onclick="saveProfile()">
                    💾 Save Profile
                </button>

            </div>
        `;

    } catch (error) {

        console.error(error);

        main.innerHTML = `
            <div class="card">
                <h2>
                    ❌ Failed to load profile
                </h2>
            </div>
        `;
    }
}


async function saveProfile() {

    const profile = {

        name:
            document.getElementById("name").value,

        email:
            document.getElementById("email").value,

        phone:
            document.getElementById("phone").value,

        college:
            document.getElementById("college").value,

        course:
            document.getElementById("course").value,

        semester:
            document.getElementById("semester").value,

        city:
            document.getElementById("city").value,

        goals:
            document.getElementById("goals").value
    };


    try {

        const data =
            await fetchJSON(
                `${API}/profile`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(profile)
                }
            );


        alert(
            data.message ||
            "Profile saved successfully!"
        );

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to save profile."
        );
    }
}


/* =========================================================
   TIMETABLE
   ========================================================= */

async function showTimetable() {

    try {

        const data =
            await fetchJSON(
                `${API}/timetable`
            );


        const rows =
            data.map(
                item => `

                    <tr>

                        <td>
                            ${escapeHtml(item.day)}
                        </td>

                        <td>
                            ${escapeHtml(item.start_time)}
                        </td>

                        <td>
                            ${escapeHtml(item.end_time)}
                        </td>

                        <td>
                            ${escapeHtml(item.subject)}
                        </td>

                        <td>
                            ${escapeHtml(item.location)}
                        </td>

                        <td>

                            <button
                                onclick="deleteClass(${item.id})"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>
                `
            ).join("");


        main.innerHTML = `

            <h1>
                📅 Timetable
            </h1>

            <div class="card">

                <h2>
                    Add New Class
                </h2>

                <input id="day" placeholder="Day">

                <input id="start" placeholder="Start Time">

                <input id="end" placeholder="End Time">

                <input id="subject" placeholder="Subject">

                <input id="location" placeholder="Location">

                <button onclick="addClass()">
                    ➕ Add Class
                </button>

                <hr>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>Day</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Subject</th>
                                <th>Location</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        main.innerHTML = `
            <div class="card">
                <h2>
                    ❌ Failed to load timetable
                </h2>

                <p>
                    ${escapeHtml(error.message)}
                </p>
            </div>
        `;
    }
}


async function addClass() {

    const data = {

        day:
            document.getElementById("day").value,

        start_time:
            document.getElementById("start").value,

        end_time:
            document.getElementById("end").value,

        subject:
            document.getElementById("subject").value,

        location:
            document.getElementById("location").value
    };


    try {

        const result =
            await fetchJSON(
                `${API}/timetable`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        alert(
            result.message ||
            "Class added successfully!"
        );


        showTimetable();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to add class."
        );
    }
}


async function deleteClass(id) {

    try {

        const data =
            await fetchJSON(
                `${API}/timetable/${id}`,
                {
                    method: "DELETE"
                }
            );


        alert(
            data.message ||
            "Class deleted."
        );


        showTimetable();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to delete class."
        );
    }
}


/* =========================================================
   ASSIGNMENTS
   ========================================================= */

async function showAssignments() {

    try {

        const data =
            await fetchJSON(
                `${API}/assignments`
            );


        const rows =
            data.map(
                item => `

                    <tr>

                        <td>
                            ${escapeHtml(item.subject)}
                        </td>

                        <td>
                            ${escapeHtml(item.title)}
                        </td>

                        <td>
                            ${escapeHtml(item.deadline)}
                        </td>

                        <td>

                            <span class="status-badge">
                                ${escapeHtml(
                                    item.status ||
                                    "Pending"
                                )}
                            </span>

                        </td>

                        <td>

                            <button
                                onclick="completeAssignment(${item.id})"
                            >
                                Complete
                            </button>

                            <button
                                onclick="deleteAssignment(${item.id})"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>
                `
            ).join("");


        main.innerHTML = `

            <h1>
                📚 Assignments
            </h1>

            <div class="card">

                <h2>
                    Add Assignment
                </h2>

                <input
                    id="assignment-subject"
                    placeholder="Subject"
                >

                <input
                    id="assignment-title"
                    placeholder="Assignment Title"
                >

                <input
                    id="assignment-deadline"
                    type="date"
                >

                <button id="addAssignmentBtn">
                    ➕ Add Assignment
                </button>

                <hr>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>Subject</th>
                                <th>Title</th>
                                <th>Deadline</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;


        document
            .getElementById("addAssignmentBtn")
            .addEventListener(
                "click",
                addAssignment
            );

    } catch (error) {

        console.error(error);

        main.innerHTML = `
            <div class="card">
                <h2>
                    ❌ Failed to load assignments
                </h2>
            </div>
        `;
    }
}


async function addAssignment() {

    const data = {

        subject:
            document
                .getElementById("assignment-subject")
                .value
                .trim(),

        title:
            document
                .getElementById("assignment-title")
                .value
                .trim(),

        deadline:
            document
                .getElementById("assignment-deadline")
                .value
    };


    if (
        !data.subject ||
        !data.title ||
        !data.deadline
    ) {

        alert(
            "Please fill all assignment fields."
        );

        return;
    }


    try {

        const result =
            await fetchJSON(
                `${API}/assignments`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        alert(
            result.message ||
            "Assignment added successfully!"
        );


        showAssignments();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to add assignment."
        );
    }
}


async function completeAssignment(id) {

    try {

        const data =
            await fetchJSON(
                `${API}/assignments/${id}`,
                {
                    method: "PUT"
                }
            );


        alert(
            data.message ||
            "Assignment completed."
        );


        showAssignments();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to complete assignment."
        );
    }
}


async function deleteAssignment(id) {

    try {

        const data =
            await fetchJSON(
                `${API}/assignments/${id}`,
                {
                    method: "DELETE"
                }
            );


        alert(
            data.message ||
            "Assignment deleted."
        );


        showAssignments();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to delete assignment."
        );
    }
}


/* =========================================================
   TASKS
   ========================================================= */

async function showTasks() {

    try {

        const data =
            await fetchJSON(
                `${API}/tasks`
            );


        const rows =
            data.map(
                item => `

                    <tr>

                        <td>
                            ${escapeHtml(item.task)}
                        </td>

                        <td>

                            <span class="status-badge">
                                ${escapeHtml(
                                    item.status ||
                                    "Pending"
                                )}
                            </span>

                        </td>

                        <td>

                            <button
                                onclick="completeTask(${item.id})"
                            >
                                Complete
                            </button>

                            <button
                                onclick="deleteTask(${item.id})"
                            >
                                Delete
                            </button>

                        </td>

                    </tr>
                `
            ).join("");


        main.innerHTML = `

            <h1>
                ✅ Tasks
            </h1>

            <div class="card">

                <h2>
                    Add Task
                </h2>

                <input
                    id="task"
                    placeholder="Enter Task"
                >

                <button onclick="addTask()">
                    ➕ Add Task
                </button>

                <hr>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>Task</th>
                                <th>Status</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        main.innerHTML = `
            <div class="card">
                <h2>
                    ❌ Failed to load tasks
                </h2>
            </div>
        `;
    }
}


async function addTask() {

    const input =
        document.getElementById("task");


    const task =
        input.value.trim();


    if (!task) {

        alert("Please enter a task.");

        return;
    }


    try {

        const result =
            await fetchJSON(
                `${API}/tasks`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            task: task
                        })
                }
            );


        alert(
            result.message ||
            "Task added successfully!"
        );


        showTasks();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to add task."
        );
    }
}


async function completeTask(id) {

    try {

        const data =
            await fetchJSON(
                `${API}/tasks/${id}`,
                {
                    method: "PUT"
                }
            );


        alert(
            data.message ||
            "Task completed."
        );


        showTasks();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to complete task."
        );
    }
}


async function deleteTask(id) {

    try {

        const data =
            await fetchJSON(
                `${API}/tasks/${id}`,
                {
                    method: "DELETE"
                }
            );


        alert(
            data.message ||
            "Task deleted."
        );


        showTasks();

    } catch (error) {

        console.error(error);

        alert(
            "❌ Failed to delete task."
        );
    }
}


/* =========================================================
   CALENDAR
   ========================================================= */

/* =========================================================
CALENDAR — GOOGLE CALENDAR
========================================================= */

async function showCalendar() {

    try {

        const data = await fetchJSON(`${API}/calendar`);

        

        let rows = "";

        if (!data || data.length === 0) {

            rows = `
                <tr>
                    <td colspan="4" style="text-align:center;">
                        No events found.
                    </td>
                </tr>
            `;

        } else {

            rows = data.map(item => {

                return `
                    <tr>

                        <td>
                            ${escapeHtml(item.event || "No title")}
                        </td>

                        <td>
                            ${escapeHtml(item.event_date || "")}
                        </td>

                        <td>
                            ${escapeHtml(item.event_time || "")}
                        </td>

                        <td>

                            <button
                                class="delete-btn"
                                data-event-id="${item.id}"
                                
                            >
                              🗑️ Delete
                            </button>

                        </td>

                    </tr>
                `;

            }).join("");
        }


        main.innerHTML = `

            <h1>📆 Calendar</h1>

            <div class="card">

                <h2>Add Event</h2>

                <input
                    id="event"
                    placeholder="Event"
                >

                <input
                    id="event_date"
                    type="date"
                >

                <input
                    id="event_time"
                    type="time"
                >

                <button onclick="addEvent()">
                    ➕ Add Event
                </button>

                <hr>

                <div class="table-container">

                    <table>

                        <thead>

                            <tr>
                                <th>Event</th>
                                <th>Date</th>
                                <th>Time</th>
                                <th>Action</th>
                            </tr>

                        </thead>

                        <tbody>
                            ${rows}
                        </tbody>

                    </table>

                </div>

            </div>
        `;
document.querySelectorAll(".delete-btn").forEach(button => {

    button.addEventListener("click", function () {

        const eventId =
            this.getAttribute("data-event-id");

        

        deleteEvent(eventId);
    });

});
    } catch (error) {

        console.error("CALENDAR ERROR:", error);

        main.innerHTML = `
            <div class="card">

                <h2>
                    ❌ Failed to load calendar
                </h2>

                <p>
                    ${escapeHtml(error.message || "Unknown error")}
                </p>

            </div>
        `;
    }
}


async function addEvent() {

    const title =
        document.getElementById("event").value.trim();

    const date =
        document.getElementById("event_date").value;

    const time =
        document.getElementById("event_time").value;


    if (!title || !date || !time) {

        alert(
            "Please enter event, date and time."
        );

        return;
    }


    const startDatetime =
        `${date}T${time}:00+05:30`;


    const start =
        new Date(startDatetime);


    const end =
        new Date(
            start.getTime() + 60 * 60 * 1000
        );


    const endDatetime =
        end.getFullYear() +
        "-" +
        String(end.getMonth() + 1).padStart(2, "0") +
        "-" +
        String(end.getDate()).padStart(2, "0") +
        "T" +
        String(end.getHours()).padStart(2, "0") +
        ":" +
        String(end.getMinutes()).padStart(2, "0") +
        ":00+05:30";


    const data = {

        event: title,

        start_datetime:
            startDatetime,

        end_datetime:
            endDatetime,

        description: ""
    };


    


    try {

        const result =
            await fetchJSON(
                `${API}/calendar`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(data)
                }
            );


        


        alert(
            result.message ||
            "Event added successfully!"
        );


        await showCalendar();


    } catch (error) {

        console.error(
            "ADD EVENT ERROR:",
            error
        );

        alert(
            "❌ Failed to add event: " +
            error.message
        );
    }
}

async function deleteEvent(id) {

   

    

    if (!id) {
        alert("Event ID is missing");
        return;
    }

    if (!confirm("Delete this event?")) {
        return;
    }

    try {

        

        const result = await fetchJSON(
            `${API}/calendar/${encodeURIComponent(id)}`,
            {
                method: "DELETE"
            }
        );

        

        alert(
            result.message ||
            "Event deleted successfully."
        );

        await showCalendar();

    } catch (error) {

        console.error("🔥 DELETE ERROR:", error);

        alert(
            "Delete failed: " + error.message
        );
    }
}

/* =========================================================
   EMAIL
   ========================================================= */

window.showEmail = async function () {

    main.innerHTML = `

        <div class="email-page">

            <h1>
                📧 Gmail Assistant
            </h1>

            <div class="email-card">

                <div class="email-toolbar">

                    <h2>
                        Inbox
                    </h2>

                    <div>

                        <button
                            onclick="connectGmail()"
                        >
                            🔗 Connect Gmail
                        </button>

                        <button
                            onclick="loadEmails()"
                        >
                            🔄 Refresh
                        </button>

                    </div>

                </div>


                <div id="email-list">

                    <p>
                        Loading emails...
                    </p>

                </div>

            </div>

        </div>
    `;


    await loadEmails();
};


async function loadEmails() {

    const list =
        document.getElementById("email-list");


    if (!list) {
        return;
    }


    try {

        const emails =
            await fetchJSON(
                `${API}/gmail`
            );


        if (
            !Array.isArray(emails) ||
            !emails.length
        ) {

            list.innerHTML = `
                <div class="empty-state">
                    📭 No emails found.
                </div>
            `;

            return;
        }


        list.innerHTML = "";


        emails.forEach(email => {

            const item =
                document.createElement("div");


            item.className =
                "email-item";


            item.innerHTML = `

                <div class="email-header">

                    <h3>
                        ${escapeHtml(
                            email.subject
                        )}
                    </h3>

                    <span>
                        ${escapeHtml(
                            email.date
                        )}
                    </span>

                </div>

                <p>
                    <strong>From:</strong>
                    ${escapeHtml(
                        email.from
                    )}
                </p>

                <p class="snippet">
                    ${escapeHtml(
                        email.snippet
                    )}
                </p>
            `;


            const button =
                document.createElement("button");


            button.textContent =
                "📩 Open Email";


            button.addEventListener(
                "click",
                () => openEmail(email.id)
            );


            item.appendChild(button);

            list.appendChild(item);

        });

    } catch (error) {

        console.error(
            "Gmail loading error:",
            error
        );


        list.innerHTML = `
            <div class="card">
                ❌ Failed to load emails.
                <br><br>
                ${escapeHtml(error.message)}
            </div>
        `;
    }
}


function connectGmail() {

    window.location.href =
        `${API}/auth/login`;
}


async function openEmail(id) {

    try {

        const email =
            await fetchJSON(
                `${API}/gmail/${id}`
            );


        currentEmailBody =
            email.body || "";


        currentEmailId =
            id;


        main.innerHTML = `

            <h1>
                📧 Email
            </h1>

            <div class="email-card">

                <h2>
                    ${escapeHtml(
                        email.subject
                    )}
                </h2>

                <p>
                    <b>From:</b>
                    ${escapeHtml(email.from)}
                </p>

                <p>
                    <b>Date:</b>
                    ${escapeHtml(email.date)}
                </p>

                <hr>

                <pre class="email-body">${escapeHtml(
                    email.body
                )}</pre>


                <div
                    id="email-action-buttons"
                    class="email-actions"
                >

                    <button id="summarize-btn">
                        📝 Summarize
                    </button>

                    <button id="reply-btn">
                        ✍️ Generate Reply
                    </button>

                    <button id="back-email-btn">
                        ⬅ Back
                    </button>

                </div>


                <div id="email-ai-result"></div>

            </div>
        `;


        document
            .getElementById("summarize-btn")
            .addEventListener(
                "click",
                summarizeEmail
            );


        document
            .getElementById("reply-btn")
            .addEventListener(
                "click",
                generateReply
            );


        document
            .getElementById("back-email-btn")
            .addEventListener(
                "click",
                showEmail
            );

    } catch (error) {

        console.error(
            "Open email error:",
            error
        );


        main.innerHTML = `
            <div class="card">

                <h2>
                    ❌ Failed to open email
                </h2>

                <p>
                    ${escapeHtml(error.message)}
                </p>

                <button onclick="showEmail()">
                    ⬅ Back
                </button>

            </div>
        `;
    }
}


async function summarizeEmail() {

    const result =
        document.getElementById(
            "email-ai-result"
        );


    if (!result) {
        return;
    }


    result.innerHTML = `
        <div class="card">
            🤖 AI is summarizing the email...
        </div>
    `;


    try {

        const data =
            await fetchJSON(
                `${API}/gmail/summarize`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            body:
                                currentEmailBody
                        })
                }
            );


        result.innerHTML = `
            <div class="card">

                <h3>
                    📝 AI Summary
                </h3>

                <p>
                    ${escapeHtml(
                        data.summary
                    )}
                </p>

            </div>
        `;

    } catch (error) {

        console.error(error);

        result.innerHTML = `
            <div class="card">

                ❌ Summarization failed.

                <br><br>

                ${escapeHtml(
                    error.message
                )}

            </div>
        `;
    }
}


async function generateReply() {

    const result =
        document.getElementById(
            "email-ai-result"
        );


    if (!result) {
        return;
    }


    result.innerHTML = `
        <div class="card">
            🤖 Generating reply...
        </div>
    `;


    try {

        const data =
            await fetchJSON(
                `${API}/gmail/reply`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            body:
                                currentEmailBody
                        })
                }
            );


        result.innerHTML = `

            <div class="card">

                <h3>
                    ✍️ AI Generated Reply
                </h3>

                <textarea
                    id="generated-reply"
                    class="reply-textarea"
                >${escapeHtml(
                    data.reply || ""
                )}</textarea>


                <div class="reply-actions">

                    <button
                        onclick="sendGeneratedReply()"
                    >
                        📤 Send Reply
                    </button>

                    <button
                        onclick="copyReply()"
                    >
                        📋 Copy Reply
                    </button>

                </div>

            </div>
        `;

    } catch (error) {

        console.error(error);

        result.innerHTML = `
            <div class="card">

                ❌ Failed to generate reply.

                <br><br>

                ${escapeHtml(
                    error.message
                )}

            </div>
        `;
    }
}


function copyReply() {

    const replyBox =
        document.getElementById(
            "generated-reply"
        );


    if (!replyBox) {

        alert(
            "No generated reply found."
        );

        return;
    }


    navigator.clipboard
        .writeText(replyBox.value)
        .then(
            () => alert("Reply copied! 📋")
        )
        .catch(
            () => alert("Could not copy reply.")
        );
}


async function sendGeneratedReply() {

    const replyBox =
        document.getElementById(
            "generated-reply"
        );


    if (!replyBox) {
        return;
    }


    const reply =
        replyBox.value.trim();


    if (!reply) {

        alert(
            "Reply is empty."
        );

        return;
    }


    if (!currentEmailId) {

        alert(
            "Original email ID is missing."
        );

        return;
    }


    if (!confirm("Send this reply through Gmail?")) {
        return;
    }


    try {

        const data =
            await fetchJSON(
                `${API}/gmail/send-reply`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            email_id:
                                currentEmailId,

                            body:
                                reply
                        })
                }
            );


        alert(
            data.message ||
            "Reply sent successfully!"
        );

    } catch (error) {

        console.error(
            "Send reply error:",
            error
        );


        alert(
            "❌ Failed to send reply."
        );
    }
}


/* =========================================================
   NOTIFICATIONS
   ========================================================= */

async function updateNotificationBadge() {

    try {

        const notifications =
            await fetchJSON(
                `${API}/notifications`
            );


        const notificationItem =
            [...document.querySelectorAll(".sidebar li")]
                .find(
                    item =>
                        item.innerText.includes(
                            "Notifications"
                        )
                );


        if (!notificationItem) {
            return;
        }


        const count =
            Array.isArray(notifications)
                ? notifications.length
                : 0;


        notificationItem.innerHTML =
            count > 0
                ? `
                    🔔
                    <span>Notifications</span>

                    <span class="notification-badge">
                        ${count}
                    </span>
                `
                : `
                    🔔
                    <span>Notifications</span>
                `;
    } catch (error) {

        console.error(
            "Notification badge error:",
            error
        );
    }
}


window.showNotifications =
    async function () {

        main.innerHTML = `

            <h1>
                🔔 Notifications
            </h1>

            <div id="notifications-container">

                <p>
                    Loading notifications...
                </p>

            </div>
        `;


        try {

            const notifications =
                await fetchJSON(
                    `${API}/notifications`
                );


            const container =
                document.getElementById(
                    "notifications-container"
                );


            if (!container) {
                return;
            }


            if (!notifications.length) {

                container.innerHTML = `

                    <div class="card">

                        <h2>
                            🎉 You're all caught up!
                        </h2>

                        <p>
                            No upcoming deadlines
                            or notifications.
                        </p>

                    </div>
                `;

                return;
            }


            container.innerHTML =
                notifications
                    .map(
                        notification => `

                            <div class="card notification-card">

                                <h2>

                                    ${escapeHtml(
                                        notification.icon ||
                                        "🔔"
                                    )}

                                    ${escapeHtml(
                                        notification.title
                                    )}

                                </h2>

                                <p>
                                    ${escapeHtml(
                                        notification.message
                                    )}
                                </p>

                                ${
                                    notification.date
                                        ? `
                                            <small>
                                                📅
                                                ${escapeHtml(
                                                    notification.date
                                                )}
                                            </small>
                                        `
                                        : ""
                                }

                            </div>
                        `
                    )
                    .join("");

        } catch (error) {

            console.error(error);


            const container =
                document.getElementById(
                    "notifications-container"
                );


            if (container) {

                container.innerHTML = `
                    <div class="card">
                        ❌ Failed to load notifications.
                    </div>
                `;
            }
        }
    };

async function enableNotifications() {
    

    if (!("Notification" in window)) {
        alert("❌ Browser notifications are not supported.");
        return;
    }

    

    try {
        const permission =
            await Notification.requestPermission();

        

        if (permission !== "granted") {
            alert(
                "❌ Notification permission is " +
                permission
            );
            return;
        }

        // Test notification immediately after user gesture
        new Notification(
            "AI Personal OS",
            {
                body: "🔔 Browser notifications are working!"
            }
        );

        

        // Now check actual application notifications
        await showBrowserNotifications();

    } catch (error) {
        console.error(
            "Notification error:",
            error
        );

        alert(
            "❌ Notification error: " +
            error.message
        );
    }
}

async function showBrowserNotifications() {

    if (!("Notification" in window)) {
        
        return;
    }

    if (Notification.permission !== "granted") {
        
        return;
    }

    try {

        

        const notifications =
            await fetchJSON(
                `${API}/notifications`
            );

        

        if (
            !Array.isArray(notifications) ||
            !notifications.length
        ) {
            
            return;
        }

        // Show all notifications when the app opens
notifications.forEach((notification, index) => {
    setTimeout(() => {
        new Notification(
            `AI Personal OS — ${notification.title}`,
            {
                body: notification.message,
                icon: "/favicon.ico"
            }
        );

        
    }, index * 500);
});

    } catch (error) {

        console.error(
            "❌ Failed to show browser notification:",
            error
        );
    }
}
/* =========================================================
   SETTINGS
   ========================================================= */

function showSettings() {

    main.innerHTML = `

        <h1>
            ⚙️ Settings
        </h1>

        <div class="card">

            <h2>
                AI Personal OS Settings
            </h2>

            <p>
                Manage your application settings.
            </p>

            <br>

            <button
                onclick="enableNotifications()"
            >
                🔔 Enable Browser Notifications
            </button>

        </div>
    `;
}


/* =========================================================
   CLOCK
   ========================================================= */

function updateClock() {

    const now =
        new Date();


    const dateElement =
        document.getElementById(
            "current-date"
        );


    const timeElement =
        document.getElementById(
            "current-time"
        );


    const hour =
        now.getHours();


    let greeting;


    if (hour < 12) {

        greeting =
            "☀️ Good Morning";

    } else if (hour < 17) {

        greeting =
            "🌤 Good Afternoon";

    } else {

        greeting =
            "🌙 Good Evening";
    }


    const title =
        document.getElementById(
            "greeting"
        );


    if (title) {

        title.innerText =
            `${greeting}, Akanksha Maurya`;
    }


    if (dateElement) {

        dateElement.innerText =
            now.toLocaleDateString(
                "en-IN",
                {
                    weekday: "long",
                    year: "numeric",
                    month: "long",
                    day: "numeric"
                }
            );
    }


    if (timeElement) {

        timeElement.innerText =
            now.toLocaleTimeString(
                "en-IN",
                {
                    hour: "2-digit",
                    minute: "2-digit",
                    second: "2-digit"
                }
            );
    }
}


/* =========================================================
   SIDEBAR
   ========================================================= */

function setupSidebar() {

    const sidebarItems =
        document.querySelectorAll(
            ".sidebar li"
        );


    sidebarItems.forEach(item => {

        item.addEventListener(
            "click",
            function () {

                sidebarItems.forEach(
                    i =>
                        i.classList.remove("active")
                );


                item.classList.add("active");


                const page =
                    item.innerText
                        .trim()
                        .toLowerCase();


                if (page.includes("dashboard")) {

                    showDashboard();

                } else if (page.includes("chat")) {

                    showChat();

                } else if (page.includes("documents")) {

                    showDocuments();

                } else if (page.includes("memory")) {

                    showMemory();

                } else if (page.includes("profile")) {

                    showProfile();

                } else if (page.includes("timetable")) {

                    showTimetable();

                } else if (page.includes("assignments")) {

                    showAssignments();

                } else if (page.includes("tasks")) {

                    showTasks();

                } else if (page.includes("calendar")) {

                    showCalendar();

                } else if (page.includes("email")) {

                    showEmail();

                } else if (page.includes("notifications")) {

                    showNotifications();

                } else if (page.includes("settings")) {

                    showSettings();
                }

            }
        );

    });
}


/* =========================================================
   STARTUP
   ========================================================= */

window.addEventListener(
    "DOMContentLoaded",
    async function () {

        


        setupSidebar();


        await showDashboard();


        updateClock();


        setInterval(
            updateClock,
            1000
        );


        
       updateNotificationBadge();

if (
    "Notification" in window &&
    Notification.permission === "granted"
) {
    showBrowserNotifications();
}

setInterval(
    updateNotificationBadge,
    60000
); 

    }
);
