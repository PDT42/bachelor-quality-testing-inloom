import { Component, Input, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { TestDataSet } from 'src/app/classes/test-data-set';
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-listtestdatasets',
  templateUrl: './list-test-data-sets.component.html',
  styleUrls: ['./list-test-data-sets.component.css'],
})
export class ListTestTataSetsComponent implements OnInit {
  @Input()
  testDataSets$: Observable<TestDataSet[]>;

  constructor(public metaEvalService: MetaEvalService) {}

  ngOnInit(): void {}

  getPtDifferenceColor(testDataSetId: string): Observable<string> {
    let color$: Observable<string> = new Observable((sub) => {
      this.metaEvalService
        .getComparisonPctDiff(testDataSetId, 'latest-auto-eval' + 'avg-man-eval')
        .subscribe((pctDiff: number) => {
          if (pctDiff < 5) {
            sub.next('#358f17');
          } else if (5 <= pctDiff && pctDiff < 10) {
            sub.next('#ebda46');
          } else if (10 <= pctDiff && pctDiff < 15) {
            sub.next('#c71c10');
          } else {
            sub.next('#6e1212');
          }
        });
    });
    return color$;
  }
}
