import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Subject, Observable } from "rxjs";
import { Configuration, Surprise } from '../models/configuration';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private configurationData = new Subject<any>();
  private supriseData = new Subject<any>();
  constructor(private http: HttpClient) { }

  getConfigurationListener() {
    return this.configurationData.asObservable();
  }

  sendConfiguration(configuration: Configuration) {
    this.http
      .post("http://localhost:3000/post", configuration)
      .subscribe(
        (surpriseData: Surprise) => {
          console.log(surpriseData)
          this.supriseData.next(surpriseData)
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
