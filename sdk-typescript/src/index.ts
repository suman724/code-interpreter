export interface ClientConfig {
  baseUrl: string;
  token: string;
}

export class CodeInterpreterClient {
  private readonly config: ClientConfig;

  constructor(config: ClientConfig) {
    this.config = config;
  }

  private headers(): HeadersInit {
    return {
      Authorization: `Bearer ${this.config.token}`,
      "Content-Type": "application/json",
    };
  }

  async createSession(payload: Record<string, unknown>): Promise<unknown> {
    const response = await fetch(`${this.config.baseUrl}/v1/sessions`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Create session failed: ${response.status}`);
    }
    return response.json();
  }

  async runCode(sessionId: string, payload: Record<string, unknown>): Promise<unknown> {
    const response = await fetch(`${this.config.baseUrl}/v1/sessions/${sessionId}/executions`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Run code failed: ${response.status}`);
    }
    return response.json();
  }

  async uploadUrl(sessionId: string, payload: Record<string, unknown>): Promise<unknown> {
    const response = await fetch(`${this.config.baseUrl}/v1/sessions/${sessionId}/files:upload-url`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Upload URL failed: ${response.status}`);
    }
    return response.json();
  }

  async downloadUrl(sessionId: string, payload: Record<string, unknown>): Promise<unknown> {
    const response = await fetch(`${this.config.baseUrl}/v1/sessions/${sessionId}/files:download-url`, {
      method: "POST",
      headers: this.headers(),
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Download URL failed: ${response.status}`);
    }
    return response.json();
  }

  async uploadFile(sessionId: string, path: string, data: ArrayBuffer): Promise<unknown> {
    const response = await fetch(
      `${this.config.baseUrl}/v1/sessions/${sessionId}/files/${path.replace(/^\\//, "")}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${this.config.token}`,
          "Content-Type": "application/octet-stream",
        },
        body: data,
      },
    );
    if (!response.ok) {
      throw new Error(`Upload file failed: ${response.status}`);
    }
    return response.json();
  }

  async downloadFile(sessionId: string, path: string): Promise<ArrayBuffer> {
    const response = await fetch(
      `${this.config.baseUrl}/v1/sessions/${sessionId}/files/${path.replace(/^\\//, "")}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${this.config.token}`,
        },
      },
    );
    if (!response.ok) {
      throw new Error(`Download file failed: ${response.status}`);
    }
    return response.arrayBuffer();
  }

  async closeSession(sessionId: string): Promise<void> {
    const response = await fetch(`${this.config.baseUrl}/v1/sessions/${sessionId}`, {
      method: "DELETE",
      headers: this.headers(),
    });
    if (!response.ok) {
      throw new Error(`Close session failed: ${response.status}`);
    }
  }
}
