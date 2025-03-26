function startSimulation() {
    const frames = parseInt(document.getElementById("frames").value);
    const reference = document.getElementById("reference").value.split(" ").map(Number);
    const algorithm = document.getElementById("algorithm").value;
    
    let memory = [];
    let index = 0;
    let summaryLog = [`Algorithm Used: ${algorithm.toUpperCase()}`, "Steps:"];
    let memoryUsageLog = [];

    function step() {
        if (index >= reference.length) {
            displaySummary(summaryLog, memoryUsageLog);
            return;
        }

        let num = reference[index];
        let removed = null;
        
        if (!memory.includes(num)) {
            if (memory.length < frames) {
                memory.push(num);
            } else {
                removed = memory.shift();
                memory.push(num);
            }
        }

        let memoryUsage = `Step ${index + 1}: ${memory.join(", ")} (Used: ${memory.length}/${frames})`;
        memoryUsageLog.push(memoryUsage);

        updateUI(memory, num, removed, memory.length, frames);
        summaryLog.push(`Entered: ${num}, Removed: ${removed || "None"}`);

        index++;
        setTimeout(step, 1500); // Slower simulation
    }

    step();
}

function updateUI(memory, entering, removed, used, total) {
    const frameContainer = document.getElementById("frames-container");
    frameContainer.innerHTML = "";

    memory.forEach(num => {
        const div = document.createElement("div");
        div.className = "frame";
        div.textContent = num;
        if (num === entering) div.classList.add("active-frame");
        frameContainer.appendChild(div);
    });

    document.getElementById("enter-popup").textContent = `Entering: ${entering}`;
    document.getElementById("remove-popup").textContent = removed ? `Removed: ${removed}` : "Removed: None";
}

function displaySummary(summaryLog, memoryUsageLog) {
    document.getElementById("summary-box").style.display = "block";
    document.getElementById("summary-content").innerHTML = summaryLog.join("<br>");
    document.getElementById("memory-content").innerHTML = memoryUsageLog.join("<br>");
}
