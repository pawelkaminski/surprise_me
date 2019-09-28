import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Subject, Observable } from "rxjs";
import { Configuration, Surprise } from '../models/configuration';

@Injectable({
  providedIn: 'root'
})
export class DatabaseService {
  private configurationData = new Subject<any>();
  private surpriseData = new Subject<any>();
  constructor(private http: HttpClient) { }

  getConfigurationListener() {
    return this.configurationData.asObservable();
  }

  getSurpriseListener() {
    return this.surpriseData.asObservable();
  }

  sendConfiguration(configuration: Configuration) {
    this.http
      .post("http://35.180.243.173:8000/api/offer/", configuration)
      .subscribe(
        (surpriseData: Surprise) => {
          console.log(surpriseData)
          this.surpriseData.next(surpriseData)
        },
        err => console.error(err)
      );
  }

  setSurprise() {
    const dummy: Surprise = { departure_schedule: "2019-12-08", departure_location: "Zurich HB", arrival_schedule: "2019-12-08", arrival_location: "Zurich HB", price: "30", participants: 2, surprise_name: "Hiking like a viking", event_name: "This-is-an-event-name Festival", event_description: "This is a description" }
    this.surpriseData.next(dummy)
  }
}
