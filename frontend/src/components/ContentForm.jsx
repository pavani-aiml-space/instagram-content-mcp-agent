import { useState } from 'react';
import { generateAndPost, createUser } from '../services/api';
import './ContentForm.css';

const FORMATS = [
  { value: '', label: 'Auto' },
  { value: 'post', label: 'Post' },
  { value: 'story', label: 'Story' },
  { value: 'reel', label: 'Reel', disabled: true, title: 'Not supported yet: Reels need a video and this pipeline only generates images.' },
];

const STEP_LABELS = {
  1: 'Content',
  2: 'Image',
  3: 'Instagram',
};

function StatusIcon({ status }) {
  if (status === 'completed') {
    return (
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4 10l4 4 8-8" />
      </svg>
    );
  }
  if (status === 'error') {
    return (
      <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 5l10 10M15 5L5 15" />
      </svg>
    );
  }
  return <span className="step-spinner" />;
}

function Stepper({ progress }) {
  const byStep = {};
  progress.forEach((entry) => {
    if (entry.step !== '0') byStep[entry.step] = entry;
  });

  return (
    <div className="stepper">
      {Object.keys(STEP_LABELS).map((step, index) => {
        const entry = byStep[step];
        const status = entry?.status ?? 'idle';
        return (
          <div className={`step step-${status}`} key={step}>
            <div className="step-marker">
              <StatusIcon status={status} />
            </div>
            <div className="step-body">
              <div className="step-label">{STEP_LABELS[step]}</div>
              {entry?.message && <div className="step-message">{entry.message}</div>}
            </div>
            {index < Object.keys(STEP_LABELS).length - 1 && <div className="step-connector" />}
          </div>
        );
      })}
    </div>
  );
}

export default function ContentForm() {
  const [formData, setFormData] = useState({
    topic: '',
    topic_details: '',
    format: '',
    user_id: '',
  });
  const [dryRun, setDryRun] = useState(true);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [progress, setProgress] = useState([]);
  const [userMessage, setUserMessage] = useState(null);
  const [creatingUser, setCreatingUser] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    setProgress([{ step: '0', agent: 'System', status: 'starting', message: 'Connecting to the agent pipeline…' }]);

    const data = {
      topic: formData.topic,
      user_id: formData.user_id,
      dry_run: dryRun,
    };
    if (formData.topic_details) data.topic_details = formData.topic_details;
    if (formData.format) data.format = formData.format;

    try {
      const response = await generateAndPost(data);
      if (response.progress_log) setProgress(response.progress_log);
      setResult(response);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async () => {
    const username = formData.user_id.trim() || 'test_user';
    setUserMessage(null);
    setError(null);
    setCreatingUser(true);
    try {
      const response = await createUser({ username, instagramUserId: username });
      setFormData((prev) => ({ ...prev, user_id: username }));
      setUserMessage({ ok: true, text: `${response.message}, using User ID "${username}".` });
    } catch (err) {
      setUserMessage({ ok: false, text: err.message || 'Failed to create user.' });
    } finally {
      setCreatingUser(false);
    }
  };

  const showProgress = progress.length > 0;

  return (
    <div className="page">
      <section className="card">
        <form onSubmit={handleSubmit} className="form">
          <div className="field">
            <label htmlFor="topic">Topic</label>
            <input
              id="topic"
              type="text"
              name="topic"
              value={formData.topic}
              onChange={handleChange}
              placeholder="e.g. Embeddings, LLM, RAG"
              required
            />
          </div>

          <div className="field">
            <label htmlFor="topic_details">
              Details <span className="label-optional">Optional</span>
            </label>
            <textarea
              id="topic_details"
              name="topic_details"
              value={formData.topic_details}
              onChange={handleChange}
              placeholder="Add context or specific points to cover: helps generate more accurate content and imagery."
              rows="3"
            />
          </div>

          <div className="field">
            <label>Format</label>
            <div className="segmented" role="radiogroup" aria-label="Content format">
              {FORMATS.map((f) => (
                <button
                  type="button"
                  key={f.value}
                  role="radio"
                  aria-checked={formData.format === f.value}
                  className={formData.format === f.value ? 'segmented-option active' : 'segmented-option'}
                  onClick={() => setFormData((prev) => ({ ...prev, format: f.value }))}
                  disabled={f.disabled}
                  title={f.title}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          <div className="field">
            <label htmlFor="user_id">User ID</label>
            <div className="input-with-action">
              <input
                id="user_id"
                type="text"
                name="user_id"
                value={formData.user_id}
                onChange={handleChange}
                placeholder="e.g. user_123"
                required
              />
              <button
                type="button"
                className="ghost-btn"
                onClick={handleCreateUser}
                disabled={creatingUser}
              >
                {creatingUser ? 'Creating…' : 'Create test user'}
              </button>
            </div>
          </div>

          {userMessage && (
            <div className={`inline-note ${userMessage.ok ? 'inline-note-success' : 'inline-note-error'}`}>
              {userMessage.text}
            </div>
          )}

          <label className="switch-row" htmlFor="dry_run">
            <span
              className={`switch ${dryRun ? 'switch-on' : ''}`}
              onClick={() => setDryRun((v) => !v)}
              role="switch"
              aria-checked={dryRun}
              tabIndex={0}
              onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setDryRun((v) => !v)}
            >
              <span className="switch-thumb" />
            </span>
            <span className="switch-label">
              <strong>Dry run</strong>
              <span className="switch-sublabel">
                {dryRun ? "Won't publish to Instagram, safe for testing the pipeline." : 'Will publish live to Instagram.'}
              </span>
            </span>
          </label>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Generating…' : dryRun ? 'Run (dry run)' : 'Generate & post to Instagram'}
          </button>
        </form>
      </section>

      {showProgress && (
        <section className="card">
          <h2 className="card-title">Progress</h2>
          <Stepper progress={progress} />
        </section>
      )}

      {result && (
        <section className="card result-card">
          <div className="result-header">
            <span className={`badge ${result.status === 'success' ? 'badge-success' : 'badge-neutral'}`}>
              {result.post_id?.startsWith('DRYRUN-') ? 'Dry run' : 'Published'}
            </span>
            <h2 className="card-title">{result.message}</h2>
          </div>

          <div className="result-body">
            {result.image_url && (
              <img className="result-image" src={result.image_url} alt="Generated content preview" />
            )}
            <div className="result-details">
              {result.content_preview && <p className="result-caption">{result.content_preview}</p>}
              <dl className="meta-list">
                <div>
                  <dt>Format</dt>
                  <dd>{result.format}</dd>
                </div>
                <div>
                  <dt>Post ID</dt>
                  <dd className="mono">{result.post_id}</dd>
                </div>
              </dl>
            </div>
          </div>

          <details className="tech-details">
            <summary>Technical details</summary>
            <pre>{JSON.stringify(result, null, 2)}</pre>
          </details>
        </section>
      )}

      {error && (
        <section className="card">
          <div className="alert alert-error">
            <div className="alert-title">Something went wrong</div>
            <div className="alert-message">{typeof error.message === 'string' ? error.message : JSON.stringify(error.message)}</div>
            {error.status ? <div className="alert-meta">Status {error.status} {error.statusText}</div> : null}
          </div>
          {error.data && (
            <details className="tech-details">
              <summary>Technical details</summary>
              <pre>{JSON.stringify(error.data, null, 2)}</pre>
            </details>
          )}
        </section>
      )}
    </div>
  );
}
