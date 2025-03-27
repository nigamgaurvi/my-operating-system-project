import streamlit as st
import time
from collections import deque, Counter
import streamlit.components.v1 as components
import pandas as pd

# Page Replacement Algorithms
def fifo_page_replacement(pages, n_frames):
    frames = []
    page_faults = 0
    steps = []
    
    for page in pages:
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
        steps.append(frames.copy())
    return steps, page_faults

def lru_page_replacement(pages, n_frames):
    frames = []
    page_faults = 0
    steps = []
    recent = []  # Tracks the order of page usage
    
    for page in pages:
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
            else:
                lru_page = min(recent, key=recent.index)
                frames.remove(lru_page)
                recent.remove(lru_page)
                frames.append(page)
                page_faults += 1
        else:
            recent.remove(page)
        recent.append(page)
        steps.append(frames.copy())
    return steps, page_faults

def optimal_page_replacement(pages, n_frames):
    frames = []
    page_faults = 0
    steps = []
    
    for i, page in enumerate(pages):
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
            else:
                future = pages[i+1:]
                farthest = -1
                replace_idx = 0
                for j, f in enumerate(frames):
                    if f not in future:
                        replace_idx = j
                        break
                    idx = future.index(f)
                    if idx > farthest:
                        farthest = idx
                        replace_idx = j
                frames[replace_idx] = page
            page_faults += 1
        steps.append(frames.copy())
    return steps, page_faults

def second_chance_page_replacement(pages, n_frames):
    frames = []
    ref_bits = {}
    page_faults = 0
    steps = []
    pointer = 0
    
    for page in pages:
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
                ref_bits[page] = 1
            else:
                while ref_bits[frames[pointer]] == 1:
                    ref_bits[frames[pointer]] = 0
                    pointer = (pointer + 1) % n_frames
                del ref_bits[frames[pointer]]
                frames[pointer] = page
                ref_bits[page] = 1
                pointer = (pointer + 1) % n_frames
            page_faults += 1
        else:
            ref_bits[page] = 1
        steps.append(frames.copy())
    return steps, page_faults

def lfu_page_replacement(pages, n_frames):
    frames = []
    page_faults = 0
    steps = []
    freq = Counter()
    
    for page in pages:
        freq[page] += 1
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
            else:
                lfu_page = min(frames, key=lambda x: freq[x])
                frames[frames.index(lfu_page)] = page
            page_faults += 1
        steps.append(frames.copy())
    return steps, page_faults

def mfu_page_replacement(pages, n_frames):
    frames = []
    page_faults = 0
    steps = []
    freq = Counter()
    
    for page in pages:
        freq[page] += 1
        if page not in frames:
            if len(frames) < n_frames:
                frames.append(page)
            else:
                mfu_page = max(frames, key=lambda x: freq[x])
                frames[frames.index(mfu_page)] = page
            page_faults += 1
        steps.append(frames.copy())
    return steps, page_faults

# Animation function with fixed rendering using st.components.v1.html
def animate_simulation(pages, steps, n_frames):
    st.subheader("Step-by-Step Simulation")
    placeholder = st.empty()
    frame_display = ["-" for _ in range(n_frames)]
    
    # CSS for animations and styling
    css = """
    <style>
    @keyframes slideIn {
        0% { transform: translateY(-100px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    @keyframes slideInLeft {
        0% { transform: translateX(-100px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    .frame-box {
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        border-radius: 10px;
        margin: 5px;
    }
    .page-box {
        width: 50px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
        border-radius: 10px;
        margin-right: 20px;
    }
    .container {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .frames {
        display: flex;
        justify-content: center;
        gap: 10px;
    }
    </style>
    """
    
    for i, (page, frame_state) in enumerate(zip(pages, steps)):
        with placeholder.container():
            st.write(f"Step {i+1}: Processing Page {page}")
            
            # Update frame display
            frame_display[:len(frame_state)] = frame_state
            frame_display[len(frame_state):] = ["-" for _ in range(n_frames - len(frame_state))]
            
            # Create the layout with page on the left and frames on the right
            html_content = css + "<div class='container'>"
            
            # Page being processed (animated from the left)
            html_content += f"""
            <div class='page-box' style='background-color: #66FF66; animation: slideInLeft 0.5s ease;'>
                {page}
            </div>
            """
            
            # Frames display
            html_content += "<div class='frames'>"
            for j, frame in enumerate(frame_display):
                if frame == page and (i == 0 or frame_state != steps[i-1]):
                    # New page entering (fault) - animate with red
                    html_content += f"""
                    <div class='frame-box' style='background-color: #FF6666; animation: slideIn 0.5s ease;'>
                        {frame}
                    </div>
                    """
                elif frame != "-":
                    # Existing page (hit) - green box
                    html_content += f"""
                    <div class='frame-box' style='background-color: #66FF66;'>
                        {frame}
                    </div>
                    """
                else:
                    # Empty slot - gray box
                    html_content += f"""
                    <div class='frame-box' style='background-color: #CCCCCC;'>
                        -
                    </div>
                    """
            html_content += "</div></div>"
            
            # Use st.components.v1.html to render the HTML
            components.html(html_content, height=150)
            
            # Status
            status = "<span style='color:red'>Page Fault</span>" if (i == 0 or frame_state != steps[i-1]) else "<span style='color:green'>Page Hit</span>"
            st.markdown(status, unsafe_allow_html=True)
            
            time.sleep(1)  # Slower delay for dramatic effect

# Function to run the simulation for a single algorithm
def run_simulation(algo, ref_string, n_frames):
    pages = [int(x.strip()) for x in ref_string.split(",")]
    total_pages = len(pages)
    
    # Algorithm Selection
    algorithms = {
        "FIFO": fifo_page_replacement,
        "LRU": lru_page_replacement,
        "Optimal": optimal_page_replacement,
        "Second Chance": second_chance_page_replacement,
        "LFU": lfu_page_replacement,
        "MFU": mfu_page_replacement
    }
    steps, page_faults = algorithms[algo](pages, n_frames)
    
    # Run animation
    animate_simulation(pages, steps, n_frames)
    
    # Summary with all steps
    st.subheader("Summary")
    page_hits = total_pages - page_faults
    hit_ratio = (page_hits / total_pages) * 100 if total_pages > 0 else 0
    
    st.write(f"**Total Page Faults**: {page_faults}")
    
    st.write("**All Steps**:")
    for i, (page, frame_state) in enumerate(zip(pages, steps)):
        status = "Page Fault" if (i == 0 or frame_state != steps[i-1]) else "Page Hit"
        st.write(f"Step {i+1}: Page {page} -> Frames: {frame_state} ({status})")
    
    st.write(f"**Page Hit Ratio**: {hit_ratio:.2f}%")
    st.write(f"**Final Frame State**: {steps[-1]}")

# Function to compare all algorithms
def compare_algorithms(ref_string, n_frames):
    pages = [int(x.strip()) for x in ref_string.split(",")]
    total_pages = len(pages)
    
    # Algorithm Selection
    algorithms = {
        "FIFO": fifo_page_replacement,
        "LRU": lru_page_replacement,
        "Optimal": optimal_page_replacement,
        "Second Chance": second_chance_page_replacement,
        "LFU": lfu_page_replacement,
        "MFU": mfu_page_replacement
    }
    
    # Store results for comparison
    comparison_data = []
    
    for algo_name, algo_func in algorithms.items():
        steps, page_faults = algo_func(pages, n_frames)
        page_hits = total_pages - page_faults
        hit_ratio = (page_hits / total_pages) * 100 if total_pages > 0 else 0
        final_frame_state = steps[-1] if steps else []
        
        comparison_data.append({
            "Algorithm": algo_name,
            "Total Page Faults": page_faults,
            "Page Hit Ratio (%)": f"{hit_ratio:.2f}",
            "Final Frame State": str(final_frame_state)
        })
    
    # Create a DataFrame for the comparison table
    df = pd.DataFrame(comparison_data)
    
    # Display the comparison table
    st.subheader("Comparison of All Algorithms")
    st.table(df)

# Main Streamlit App
def main():
    st.title("Page Replacement Algorithm Simulator")
    
    # Initialize session state
    if 'run_simulation' not in st.session_state:
        st.session_state.run_simulation = False
    if 'run_comparison' not in st.session_state:
        st.session_state.run_comparison = False
    if 'algo' not in st.session_state:
        st.session_state.algo = "FIFO"
    if 'ref_string' not in st.session_state:
        st.session_state.ref_string = ""
    if 'n_frames' not in st.session_state:
        st.session_state.n_frames = 3

    # User Inputs
    algo = st.sidebar.selectbox(
        "Select Algorithm",
        ["FIFO", "LRU", "Optimal", "Second Chance", "LFU", "MFU"],
        index=["FIFO", "LRU", "Optimal", "Second Chance", "LFU", "MFU"].index(st.session_state.algo)
    )
    ref_string = st.text_input("Enter Reference String (comma-separated)", st.session_state.ref_string)
    n_frames = st.number_input("Number of Frames", min_value=1, max_value=10, value=st.session_state.n_frames)

    # Update session state with user inputs
    st.session_state.algo = algo
    st.session_state.ref_string = ref_string
    st.session_state.n_frames = int(n_frames)

    # Run simulation if triggered
    if st.button("Run Simulation"):
        st.session_state.run_simulation = True
        st.session_state.run_comparison = False  # Reset comparison state

    # Replay simulation button
    if st.session_state.run_simulation and st.button("Replay Simulation"):
        st.session_state.run_simulation = True
        st.session_state.run_comparison = False  # Reset comparison state

    # Compare algorithms button
    if st.button("Compare Algorithms"):
        st.session_state.run_simulation = False  # Reset simulation state
        st.session_state.run_comparison = True

    # Execute simulation if run_simulation is True
    if st.session_state.run_simulation:
        run_simulation(st.session_state.algo, st.session_state.ref_string, st.session_state.n_frames)

    # Execute comparison if run_comparison is True
    if st.session_state.run_comparison:
        compare_algorithms(st.session_state.ref_string, st.session_state.n_frames)

if __name__ == "__main__":
    main()