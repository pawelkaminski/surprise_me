import { Injectable } from "@angular/core";
import * as $ from "jquery";
import { Subject, Observable } from "rxjs";
import { DatabaseService } from "./database.service";

@Injectable({
  providedIn: "root"
})
export class AnimationsService {
  spinner = new Subject<any>();
  constructor(private dbService: DatabaseService) { }

  spinnerListener() {
    return this.spinner.asObservable();
  }

  spinnerState(state: Boolean) {
    this.spinner.next(state);
    setTimeout(() => {
      this.spinner.next(0);
      this.dbService.setSurprise()
    }, 6000)
  }
} 