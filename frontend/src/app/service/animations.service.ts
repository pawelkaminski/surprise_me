import { Injectable } from "@angular/core";
import * as $ from "jquery";
import { Subject, Observable } from "rxjs";

@Injectable({
  providedIn: "root"
})
export class AnimationsService {
  spinner = new Subject<any>();
  constructor() { }

  spinnerListener() {
    return this.spinner.asObservable();
  }

  spinnerState(state: Boolean) {
    this.spinner.next(state);
  }
} 