import { stringify } from '@angular/compiler/src/util';
import { Component, Input, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Observable } from 'rxjs';
import { Evaluation } from 'src/app/classes/evaluation';
import { TestDataSet } from '../../classes/test-data-set';
import { MetaEvalService } from '../../services/metaeval.service';
import { TestDataSetService } from '../../services/test-data-set-service.service';

@Component({
  selector: 'app-multiple-comparison',
  templateUrl: './multiple-comparison.component.html',
  styleUrls: ['./multiple-comparison.component.css'],
})
export class MultipleComparisonComponent implements OnInit {
  @Input()
  metaEvals$: Observable<Map<string, Object>>;

  @Input()
  testDataSets$: Observable<TestDataSet[]>;

  @Input()
  averageMode: boolean;

  @Input()
  evaluations: Evaluation[];

  constructor(public metaEvalService: MetaEvalService) {}

  ngOnInit(): void {
    if (!this.averageMode && !this.evaluations) {
      throw new Error(
        'Cannot use individual mode without individual Evaluations!'
      );
    }
  }

  ngAfterViewInit(): void {
    this.testDataSets$.subscribe((testDataSets: TestDataSet[]) => {
      if (testDataSets.length > 0) {
        this.metaEvals$.subscribe((metaEvals: Map<string, Object>) => {
          if (metaEvals.size == testDataSets.length) {
            this.createGradesPerTestDataSetChart(metaEvals);
          }
        });
      }
    });
  }

  createGradesPerTestDataSetChart(tdsMetaEvals: Map<string, Object>) {
    const CHART_KEY = 'grades-per-test-data-set';
    const ROOT = d3.select('div#' + CHART_KEY);

    if (ROOT.size() != 0) {
      // Define Constants
      const MARGIN_VERTICAL = 20;
      const MARGIN_HORIZONTAL = 20;
      const ROOT_WIDTH = parseInt(ROOT.style('width'));
      const ROOT_HEIGHT = 400;
      const SVG_WIDTH = ROOT_WIDTH - 3 * MARGIN_HORIZONTAL;
      const SVG_HEIGHT = ROOT_HEIGHT - 2 * MARGIN_VERTICAL;

      let xItems: Array<string> = [];
      let studentGrades: Map<string, Object[]> = new Map();

      // Get the relevant grades from the meta eval
      if (this.averageMode) {
        Array.from(tdsMetaEvals.entries()).map(([_, tdsMetaEval]) => {
          xItems.push(tdsMetaEval['student-id']);
          studentGrades.set(tdsMetaEval['student-id'], [
            {
              evalType: 'A',
              grade: tdsMetaEval['eval-stats']['latest-auto-eval']['grade'],
            },
            {
              evalType: 'M',
              grade: tdsMetaEval['eval-stats']['avg-man-eval']['grade'],
            },
          ]);
        });
      } else {
        Array.from(tdsMetaEvals.entries()).map(([_, tdsMetaEval]) => {
          Object.entries(tdsMetaEval['eval-stats']).map(([key, value]) => {
            if (!['avg-man-eval', 'latest-auto-eval'].includes(key) && value['type'] != 'A') {
              let studentId: string = tdsMetaEval['student-id'];
              let created: Date = new Date(value['created'] * 1000);

              xItems.push(studentId + " - " + created.toDateString());
              studentGrades.set(
                studentId + " - " + created.toDateString(),
                [
                  {
                    evalType: 'A',
                    grade:
                      tdsMetaEval['eval-stats']['latest-auto-eval']['grade'],
                  },
                  {
                    evalType: 'M',
                    grade: value['grade'],
                  },
                ]
              );
            }
          });
        });
      }

      // Define a color scale for the
      // two possible bar colors.
      let color: Map<string, string> = new Map();
      color.set('A', '#1d7e99');
      color.set('M', '#e39127');

      // Create svg root
      let svg_root = ROOT.append('svg')
        .attr('width', ROOT_WIDTH)
        .attr('height', ROOT_HEIGHT)
        .append('g')
        .attr(
          'transform',
          'translate(' + MARGIN_VERTICAL + ', ' + MARGIN_HORIZONTAL + ')'
        );

      // Define x-scale
      let xScale = d3
        .scaleBand()
        .domain(xItems)
        .range([0, SVG_WIDTH])
        .padding(0.25);

      svg_root
        .append('g')
        .style('font', '14px roboto')
        .attr(
          'transform',
          'translate(' + MARGIN_HORIZONTAL + ', ' + SVG_HEIGHT + ')'
        )
        .call(d3.axisBottom(xScale).tickSize(0).tickPadding(6));

      // Define x-sub-scale
      let xSubScale = d3
        .scaleBand()
        .domain(['M', 'A'])
        .range([0, xScale.bandwidth()])
        .padding(0.025);

      // Define y-scale
      let yScale = d3.scaleLinear().range([SVG_HEIGHT, 0]).domain([0, 100]);

      svg_root
        .append('g')
        .style('font', '14px roboto')
        .attr('transform', 'translate(' + MARGIN_HORIZONTAL + ', 0)')
        .call(d3.axisLeft(yScale));

      // Adding values of manual eval to chart
      svg_root
        .append('g')
        .attr('transform', 'translate(' + MARGIN_HORIZONTAL + ', 0)')
        .selectAll('g')
        .data(xItems)
        .enter()
        .append('g')
        .attr('transform', (tdsKey) => {
          return 'translate(' + xScale(tdsKey) + ')';
        })
        .selectAll('rect')
        .data((studentId) => {
          return studentGrades.get(studentId);
        })
        .enter()
        .append('rect')
        .attr('x', (studentGrade) => {
          return xSubScale(studentGrade['evalType']);
        })
        .attr('y', (studentGrade) => {
          return yScale(studentGrade['grade']);
        })
        .attr('height', (studentGrade) => {
          return SVG_HEIGHT - yScale(studentGrade['grade']);
        })
        .attr('width', xSubScale.bandwidth())
        .attr('fill', (studentGrade): string => {
          if (studentGrade['evalType'] != null) {
            return color.get(studentGrade['evalType']);
          } else return null;
        });
    }
  }
}
