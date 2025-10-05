import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const healthCheck = () => api.get('/health');
export const getTracks = () => api.get('/tracks');
export const createTrack = (trackData) => api.post('/tracks', trackData);
export const getTrack = (id) => api.get(`/tracks/${id}`);
export const updateTrack = (id, trackData) => api.patch(`/tracks/${id}`, trackData);
export const deleteTrack = (id) => api.delete(`/tracks/${id}`);
