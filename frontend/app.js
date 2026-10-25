const form = document.getElementById('resume-form');
const fileInput = document.getElementById('resume-file');
const fileNameDisplay = document.getElementById('file-name');
const jobDescriptionInput = document.getElementById('job-description');
const statusElement = document.getElementById('status');
const resultsSection = document.getElementById('results');
const submitBtn = document.getElementById('analyze-button');
const scoreCircle = document.getElementById('score-circle');
const scoreText = document.getElementById('match-score');

// File Input UI update
fileInput.addEventListener('change', (e) => {
  if (e.target.files.length > 0) {
    fileNameDisplay.textContent = e.target.files[0].name;
    fileNameDisplay.style.color = 'var(--primary)';
  } else {
    fileNameDisplay.textContent = 'Select or drop your PDF here';
    fileNameDisplay.style.color = 'var(--text-muted)';
  }
});

const showStatus = (message, isError = false) => {
  statusElement.textContent = message;
  statusElement.className = isError ? 'status error' : 'status';
};

const setLoadingState = (isLoading) => {
  const btnText = submitBtn.querySelector('.btn-text');
  const btnIcon = submitBtn.querySelector('i');
  
  submitBtn.disabled = isLoading;
  
  if (isLoading) {
    btnText.textContent = 'Processing...';
    btnIcon.className = 'fas fa-spinner fa-spin';
  } else {
    btnText.textContent = 'Initialize Analysis';
    btnIcon.className = 'fas fa-microchip';
  }
};

// Logic to determine color based on percentage
const getScoreColor = (score) => {
  if (score < 40) return 'var(--score-low)';    // 0-39% Red
  if (score < 70) return 'var(--score-medium)'; // 40-69% Yellow/Amber
  return 'var(--score-high)';                   // 70-100% Green
};

// Animate score number AND circular progress ring
const animateScore = (targetScore) => {
  let currentScore = 0;
  const duration = 1500; 
  const interval = 20; 
  const steps = duration / interval;
  const increment = targetScore / steps;
  
  const activeColor = getScoreColor(targetScore);
  const emptyColor = 'var(--score-empty)';

  scoreText.style.color = activeColor; // Set text color

  const timer = setInterval(() => {
    currentScore += increment;
    
    if (currentScore >= targetScore) {
      currentScore = targetScore;
      clearInterval(timer);
    }
    
    // Update number
    scoreText.textContent = `${currentScore.toFixed(1)}%`;
    
    // Update Conic Gradient for the circular progress bar
    scoreCircle.style.background = `conic-gradient(${activeColor} ${currentScore}%, ${emptyColor} 0%)`;
    
  }, interval);
};

const renderList = (elementId, items) => {
  const list = document.getElementById(elementId);
  list.innerHTML = '';

  if (!items || items.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'None detected';
    list.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = item;
    list.appendChild(li);
  });
};

const renderResults = (payload) => {
  resultsSection.classList.remove('hidden');
  
  // Reset score ring before animating
  scoreCircle.style.background = `conic-gradient(var(--score-empty) 100%, var(--score-empty) 0%)`;
  scoreText.textContent = `0%`;

  setTimeout(() => {
    animateScore(Number(payload.match_score));
    
    renderList('matched-skills', payload.matched_skills);
    renderList('missing-skills', payload.missing_skills);
    renderList('strengths', payload.strengths);
    renderList('improvement-areas', payload.improvement_areas);
    renderList('suggestions', payload.suggestions);
    
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
};

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!fileInput.files[0]) {
    showStatus('Please choose a PDF resume before continuing.', true);
    return;
  }

  const jobDescription = jobDescriptionInput.value.trim();
  if (!jobDescription) {
    showStatus('Please paste a job description before analyzing.', true);
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  setLoadingState(true);
  showStatus('Uploading document...');

  try {
    const uploadResponse = await fetch('/resumes/upload', {
      method: 'POST',
      body: formData,
    });

    const uploadData = await uploadResponse.json();
    if (!uploadResponse.ok) {
      throw new Error(uploadData.detail || 'Resume upload failed.');
    }

    const analyzeData = new FormData();
    analyzeData.append('resume_id', String(uploadData.id));
    analyzeData.append('job_description', jobDescription);

    showStatus('Running AI analysis against requirements...');

    const analysisResponse = await fetch('/analyze', {
      method: 'POST',
      body: analyzeData,
    });

    const result = await analysisResponse.json();
    if (!analysisResponse.ok) {
      throw new Error(result.detail || 'Analysis failed.');
    }

    renderResults(result);
    showStatus('Analysis complete.');
  } catch (error) {
    showStatus(error.message, true);
  } finally {
    setLoadingState(false);
  }
});