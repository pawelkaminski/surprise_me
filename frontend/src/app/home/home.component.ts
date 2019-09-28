import { Component, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DatabaseService } from "../service/database.service";
import { Configuration } from "../models/configuration";
import { NgForm } from "@angular/forms";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"]
})
export class HomeComponent implements OnInit {
  gifListenerSub: Subscription;
  configuration: Configuration = { activity: null, departureLocation: null, schedule: null, maxPrice: null, participants: null };
  speech: String = null
  constructor(private dbService: DatabaseService) { }

  ngOnInit() {
    this.gifListenerSub = this.dbService
      .getGifListener()
      .subscribe(data => {
        this.configuration = data;
      });
  }

  speechToText() {
    console.log("this.configuration")
  }

  onSubmit() {
    console.log(this.configuration)
    this.dbService.sendConfiguration(this.configuration);
  }
}
