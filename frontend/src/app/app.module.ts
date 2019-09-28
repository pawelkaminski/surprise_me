import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { NgbModule } from "@ng-bootstrap/ng-bootstrap";
import { HttpClientModule } from "@angular/common/http";
import { NgwWowModule } from 'ngx-wow';
import { ChartsModule } from 'ng2-charts';

import { AppComponent } from "./app.component";
import { RouterModule, Routes } from "@angular/router";
import { HomeComponent } from "./home/home.component";
import { MiscellaneousComponent } from "./miscellaneous/miscellaneous.component";
import { MatButtonModule, MatCheckboxModule, MatSlideToggleModule, MatSliderModule } from "@angular/material";
import { ParticlesModule } from "angular-particle";
import { ResultCardComponent } from './home/result-card/result-card.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MiscellaneousComponent,
    ResultCardComponent
  ],
  imports: [
    BrowserModule,
    NgbModule,
    HttpClientModule,
    ParticlesModule,
    MatButtonModule,
    MatCheckboxModule,
    NgwWowModule,
    ChartsModule,
    MatSlideToggleModule,
    MatSliderModule,
    RouterModule.forRoot([
      {
        path: "",
        component: HomeComponent,
        pathMatch: "full"
      },
      {
        path: "**",
        component: MiscellaneousComponent,
        pathMatch: "full"
      }
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
