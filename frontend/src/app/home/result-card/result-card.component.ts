import { Component, OnInit } from '@angular/core';
import { AnimationsService } from 'src/app/service/animations.service';

@Component({
  selector: 'app-result-card',
  templateUrl: './result-card.component.html',
  styleUrls: ['./result-card.component.css']
})
export class ResultCardComponent implements OnInit {

  constructor(private animationService: AnimationsService) { }

  ngOnInit() {
  }

  setSpinner(state: Boolean) {
    this.animationService.spinnerState(true);
  }

}
