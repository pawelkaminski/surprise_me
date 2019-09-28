import { Component, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DatabaseService } from "../service/database.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"]
})
export class HomeComponent implements OnInit {
  gifListenerSub: Subscription;
  data = [];
  constructor(private dbService: DatabaseService) { }

  ngOnInit() {
    this.gifListenerSub = this.dbService
      .getGifListener()
      .subscribe(data => {
        this.data = data;
      });
  }
}
