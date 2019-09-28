import { Component, OnInit } from '@angular/core';
import { AnimationsService } from 'src/app/service/animations.service';
import { Surprise } from 'src/app/models/configuration';

@Component({
  selector: 'app-result-card',
  templateUrl: './result-card.component.html',
  styleUrls: ['./result-card.component.css']
})
export class ResultCardComponent implements OnInit {
  surprise: Surprise = { departure_location: null, arrival_schedule: null, arrival_location: null, price: null, participants: null, surprise_name: null, event_name: null, event_description: null };

  constructor(private animationService: AnimationsService) { }

  ngOnInit() {
  }

  setSpinner(state: Boolean) {
    this.animationService.spinnerState(true);
  }

}
