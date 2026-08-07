export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface AuthUser {
  id: number | string;
  name: string;
  email: string;
}

export interface AuthResponse {
  message: string;
  user: AuthUser;
}