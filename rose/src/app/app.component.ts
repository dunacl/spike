import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'rose';
  opened = false;
  toogleSidebar() {
    this.opened = !this.opened;
  }
}
