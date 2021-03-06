
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  baseUrl = "http://127.0.0.1:8000/";
  htttpHeaders = new HttpHeaders({ "Content-Type": "application/json" });
  // http options used for making API calls
  private httpOptions: any;
  // the actual JWT token
  public token: string;
  // the token expiration date
  public tokenExpires: Date;
  // the username of the logged in user
  public username: string;
  // error messages received from the login attempt
  public errors: any = [];

  visible: boolean;

  constructor(private http: HttpClient) { this.visible = true; }

  hide() { this.visible = false; }

  show() { this.visible = true; }


  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint


  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http.post('/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }

  private updateData(token) {
    this.token = token;
    this.errors = [];

    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.tokenExpires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }




}
