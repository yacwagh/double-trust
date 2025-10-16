import axios from 'axios';
import { Agent, Tool, DiscoveryStatus, ToolExecuteRequest, ToolExecuteResponse, ToolSelectionRequest, ToolSelectionResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Agents API
export const agentsApi = {
  getAll: (): Promise<{ agents: Agent[]; total: number }> =>
    api.get('/api/agents/').then(res => res.data),
  
  getById: (id: string): Promise<Agent> =>
    api.get(`/api/agents/${id}`).then(res => res.data),
  
  // Removed create via SDK
  
  getTools: (id: string): Promise<{ agent_id: string; tools: Tool[] }> =>
    api.get(`/api/agents/${id}/tools`).then(res => res.data),
  
  // Permissions removed
  
  getStatistics: (): Promise<any> =>
    api.get('/api/agents/statistics/overview').then(res => res.data),
};

// Tools API
export const toolsApi = {
  getAll: (): Promise<{ tools: Tool[]; total: number }> =>
    api.get('/api/tools/').then(res => res.data),
  
  getById: (id: number): Promise<Tool> =>
    api.get(`/api/tools/${id}`).then(res => res.data),
  
  getByServer: (): Promise<Record<string, Tool[]>> =>
    api.get('/api/tools/by-server').then(res => res.data),
  
  execute: (toolId: number, request: ToolExecuteRequest): Promise<ToolExecuteResponse> =>
    api.post(`/api/tools/${toolId}/execute`, request).then(res => res.data),
  
  getStatistics: (): Promise<any> =>
    api.get('/api/tools/statistics/overview').then(res => res.data),
};

// Discovery API
export const discoveryApi = {
  discoverAgents: (githubRepoUrl: string): Promise<any> =>
    api.post('/api/discovery/agents', { github_repo_url: githubRepoUrl }).then(res => res.data),
  
  
  getStatus: (): Promise<DiscoveryStatus> =>
    api.get('/api/discovery/status').then(res => res.data),
};

export default api;
