const socket = new WebSocket('ws://' + window.location.host + '/ws/research/');

const startBtn = document.getElementById('startBtn');
const taskInput = document.getElementById('taskInput');
const reportOutput = document.getElementById('reportOutput');

socket.onopen = function(e) {
    console.log("WebSocket connection established!");
};

startBtn.onclick = function() {
    const task = taskInput.value;
    if (!task) {
        alert("Please enter a research task!");
        return;
    }

    // Reset UI before starting
    reportOutput.innerHTML = "Agent is thinking...";
    reportOutput.classList.add("italic");
    
    // Start button disable karein taaki multiple requests na jayein
    startBtn.disabled = true;
    startBtn.innerText = "Researching...";

    socket.send(JSON.stringify({ 'task': task }));
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Received data:", data);

    if (data.type === 'status_update') {
        const nodeId = `status-${data.node}`; // e.g., status-planner
        const nodeElement = document.getElementById(nodeId);

        if (nodeElement) {
            // Node ko active dikhayein
            nodeElement.classList.remove('text-gray-400');
            nodeElement.classList.add('node-active', 'text-blue-600', 'font-bold');
            
            // Spinner add karein
            const iconDiv = nodeElement.querySelector('.icon');
            if (iconDiv) {
                iconDiv.innerHTML = '<div class="spinner"></div>';
            }
        }
    }

    if (data.type === 'final_report') {
        // Final report display karein
        reportOutput.innerHTML = data.report;
        reportOutput.classList.remove("italic", "text-gray-600");
        
        // Button reset karein
        startBtn.disabled = false;
        startBtn.innerText = "Start Autonomous Research";

        // Saare spinners khatam karke checkmark laga dein
        document.querySelectorAll('.icon').forEach(icon => {
            icon.innerHTML = '<span class="text-green-500">✓</span>';
        });
    }
};

socket.onclose = function(e) {
    console.error('Socket closed unexpectedly. Reconnecting...');
    // Optional: Reconnect logic
};