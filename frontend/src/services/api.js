export const API_BASE_URL = 'http://localhost:8000';

async function handleResponse(response) {
  let responseData;
  try {
    const text = await response.text();
    responseData = text ? JSON.parse(text) : {};
  } catch (e) {
    responseData = { error: 'Failed to parse response', message: response.statusText || e.message };
  }

  if (!response.ok) {
    // Extract error message from FastAPI validation errors
    let errorMessage = response.statusText;
    if (responseData.detail) {
      if (Array.isArray(responseData.detail)) {
        // Handle FastAPI validation errors array
        errorMessage = responseData.detail
          .map(d => {
            if (typeof d === 'string') return d;
            if (d.msg) return d.msg;
            if (d.message) return d.message;
            if (d.loc && d.msg) return `${d.loc.join('.')}: ${d.msg}`;
            return JSON.stringify(d);
          })
          .join(', ');
      } else if (typeof responseData.detail === 'string') {
        errorMessage = responseData.detail;
      } else if (typeof responseData.detail === 'object') {
        errorMessage = JSON.stringify(responseData.detail);
      }
    } else if (responseData.message) {
      errorMessage = responseData.message;
    } else if (responseData.error) {
      errorMessage = typeof responseData.error === 'string'
        ? responseData.error
        : JSON.stringify(responseData.error);
    }

    throw {
      status: response.status,
      statusText: response.statusText,
      data: responseData,
      message: errorMessage,
    };
  }

  return responseData;
}

async function post(path, body) {
  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    return await handleResponse(response);
  } catch (error) {
    if (error.status !== undefined) {
      throw error; // Already formatted
    }
    throw {
      status: 0,
      statusText: 'Network Error',
      data: { error: error.message || 'Failed to connect to server' },
      message: `Could not reach the backend. Make sure it's running on ${API_BASE_URL}.`,
    };
  }
}

export function generateAndPost(data) {
  return post('/api/content/generate-and-post', data);
}

export function createUser({ username, instagramUserId, accessToken = 'test_token' }) {
  return post('/api/users/create', {
    username,
    instagram_user_id: instagramUserId,
    access_token: accessToken,
  });
}
