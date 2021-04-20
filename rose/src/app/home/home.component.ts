import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

// import custom validator to validate that password and confirm password fields match
// import { MustMatch } from '../_helpers/must-match.validator';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  calculateForm: FormGroup;
  submitted = false;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
      this.calculateForm = this.formBuilder.group({
          fromStreet: ['', Validators.required],
          fromNumber: ['', Validators.required],
          fromCity: ['', Validators.required],
          fromCountry: ['', Validators.required],
          toStreet: ['', Validators.required],
          toNumber: ['', Validators.required],
          toCity: ['', Validators.required],
          toCountry: ['', Validators.required]
      }, {
          //validator: MustMatch('password', 'confirmPassword')
      });
  }

  // convenience getter for easy access to form fields
  get f() { return this.calculateForm.controls; }

  onSubmit() {
      this.submitted = true;

      // stop here if form is invalid
      if (this.calculateForm.invalid) {
          return;
      }

      // display form values on success
      alert('SUCCESS!! :-)\n\n' + JSON.stringify(this.calculateForm.value, null, 4));
  }

  onReset() {
      this.submitted = false;
      this.calculateForm.reset();
  }
}
