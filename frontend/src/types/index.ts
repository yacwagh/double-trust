export interface Agent {
  id: string;
  file_path?: string;
  role: string;
  system_prompt: string;
  model?: string;
  temperature?: number;
  framework?: string;
  risk?: 'low' | 'medium' | 'high';
  risk_reason?: string;
  created_at: string;
}

export interface Tool {
  id: number;
  name: string;
  description: string;
  parameters: Record<string, any>;
}


export interface DiscoveryStatus {
  total_agents: number;
  discovered_agents: number;
}

export interface ToolExecuteRequest {
  agent_id: string;
  parameters: Record<string, any>;
}

export interface ToolExecuteResponse {
  success: boolean;
  result?: Record<string, any>;
  error?: string;
  tool_name: string;
  server_url: string;
}

export interface ToolSelectionRequest {
  user_prompt: string;
}

export interface ToolSelectionResponse {
  selected_tool?: Tool;
  reason: string;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}
