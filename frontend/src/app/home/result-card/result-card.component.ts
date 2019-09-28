import { Component, OnInit } from '@angular/core';
import { AnimationsService } from 'src/app/service/animations.service';
import { Surprise } from 'src/app/models/configuration';
import { Subscription } from 'rxjs';
import { DatabaseService } from 'src/app/service/database.service';
import * as $ from 'jquery';

@Component({
  selector: 'app-result-card',
  templateUrl: './result-card.component.html',
  styleUrls: ['./result-card.component.css']
})
export class ResultCardComponent implements OnInit {
  surpriseListenerSub: Subscription;
  surprise: Surprise;
  spinner: Boolean = false;
  spinnerListenerSub: Subscription;

  constructor(private animationService: AnimationsService, private dbService: DatabaseService) { }

  ngOnInit() {
    this.surpriseListenerSub = this.dbService
      .getSurpriseListener()
      .subscribe(surprise => {
        this.surprise = surprise;
        console.log(surprise)
      });
    this.spinnerListenerSub = this.animationService
      .spinnerListener()
      .subscribe(spinner => {
        this.spinner = spinner;
      });
  }

  setSpinner(state: Boolean) {
    this.animationService.spinnerState(true);
  }

  flipCard() {
    console.log("helno")
    $(".flip-card-inner").css("transform", "rotateX(-180deg)")
    $(".confetti").css("opacity", "1")
    setTimeout(() => {
      $(".confetti").css("opacity", "0")
    }, 1600)
  }

}
