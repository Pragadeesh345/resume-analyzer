const form = document.getElementById('resume-form');
const fileInput = document.getElementById('resume-file');
const jobDescriptionInput = document.getElementById('job-description');
const statusElement = document.getElementById('status');
const resultsSection = document.getElementById('results');

const showStatus = (message, isError = false) => {
  statusElement.textContent = message;
  statusElement.classList.toggle('error', isError);
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
  document.getElementById('match-score').textContent = `${Number(payload.match_score).toFixed(2)}%`;
  renderList('matched-skills', payload.matched_skills);
  renderList('missing-skills', payload.missing_skills);
  renderList('strengths', payload.strengths);
  renderList('improvement-areas', payload.improvement_areas);
  renderList('suggestions', payload.suggestions);
  resultsSection.classList.remove('hidden');
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

  showStatus('Uploading resume...');

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

    showStatus('Analyzing resume against the job description...');

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
  }
});
