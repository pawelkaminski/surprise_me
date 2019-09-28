import { Component, OnInit } from "@angular/core";
import { Subscription } from "rxjs";
import { DatabaseService } from "../service/database.service";
import { Configuration, Surprise } from "../models/configuration";
import { NgForm } from "@angular/forms";
import { AnimationsService } from "../service/animations.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"]
})
export class HomeComponent implements OnInit {
  configurationListenerSub: Subscription;
  surpriseListenerSub: Subscription;
  spinnerListenerSub: Subscription;
  configuration: Configuration = { activity: null, departureLocation: null, schedule: null, maxPrice: null, participants: null };
  surprise: Surprise
  speech: String = null
  spinner: Boolean = false
  card: Boolean = false
  constructor(private dbService: DatabaseService, private animationService: AnimationsService) { }

  ngOnInit() {
    this.configurationListenerSub = this.dbService
      .getConfigurationListener()
      .subscribe(configuration => {
        this.configuration = configuration;
      });
    this.surpriseListenerSub = this.dbService
      .getConfigurationListener()
      .subscribe(surprise => {
        this.surprise = surprise;
      });
    this.spinnerListenerSub = this.animationService
      .spinnerListener()
      .subscribe(spinner => {
        this.spinner = spinner;
      });
  }

  speechToText() {
    console.log("this.configuration")
    setTimeout(() => {
      this.configuration = { activity: "Hiking", departureLocation: "Zurich HB", schedule: "2019-12-08", maxPrice: 30, participants: 1 };
    }, 1000)
  }

  onSubmit() {
    console.log(this.configuration)
    this.dbService.sendConfiguration(this.configuration);
  }


  setSpinner(state: Boolean) {
    this.animationService.spinnerState(true);
  }

}
