import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Subject, Observable } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private data = new Subject<any>();
  constructor(private http: HttpClient) { }

  getGifListener() {
    return this.data.asObservable();
  }

  post(i) {
    const context = { name: "Dummy" }
    this.http
      .post("http://localhost:3000/post", context)
      .subscribe(
        (data) => {
          console.log(data)
        },
        err => console.error(err)
      );
  }
  get(i) {
    const context = { name: "Dummy" }
    this.http
      .get("http://localhost:3000/post")
      .subscribe(
        (data) => {
          console.log(data)
        },
        err => console.error(err)
      );
  }
}
