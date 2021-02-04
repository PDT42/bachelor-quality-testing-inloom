import { Component, Input, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Observable } from 'rxjs';
import { Evaluation } from 'src/app/classes/evaluation';
import { TestDataSet } from 'src/app/classes/test-data-set';
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-exercise-level-comparison',
  templateUrl: './exercise-level-comparison.component.html',
  styleUrls: ['./exercise-level-comparison.component.css'],
})
export class ExerciseLevelComparisonComponent implements OnInit {
  @Input()
  metaEvals$: Observable<Map<string, Object>>;

  @Input()
  testDataSets$: Observable<TestDataSet[]>;

  @Input()
  comparisonKey: string;

  @Input()
  averageMode: boolean;

  @Input()
  evaluations: Evaluation[];

  avgGradeQuotientsChartCreated: boolean;
  pointDiffsChartCreated: boolean;
  pointPctDiffChartCreated: boolean;

  constructor() {}

  ngOnInit(): void {
    if (!this.averageMode && !this.evaluations) {
      throw new Error(
        'Cannot use individual mode without individual Evaluations!'
      );
    }
  }

  ngAfterViewInit(): void {}

  onTabChange(event: any) {
    if (event['index'] == 1 && !this.avgGradeQuotientsChartCreated) {
      this.testDataSets$.subscribe((testDataSets: TestDataSet[]) => {
        if (testDataSets.length > 0) {
          this.metaEvals$.subscribe((metaEvals: Map<string, Object>) => {
            if (metaEvals.size == testDataSets.length) {
              this.createRegularBarChart(
                metaEvals,
                'grade-quotients-pct',
                false
              );
              this.avgGradeQuotientsChartCreated = true;
            }
          });
        }
      });
    }
    if (event['index'] == 2 && !this.pointDiffsChartCreated) {
      this.testDataSets$.subscribe((testDataSets: TestDataSet[]) => {
        if (testDataSets.length > 0) {
          this.metaEvals$.subscribe((metaEvals: Map<string, Object>) => {
            if (metaEvals.size == testDataSets.length) {
              this.createRegularBarChart(metaEvals, 'point-diffs', true);
              this.pointDiffsChartCreated = true;
            }
          });
        }
      });
    }
    if (event['index'] == 3 && !this.pointPctDiffChartCreated) {
      this.testDataSets$.subscribe((testDataSets: TestDataSet[]) => {
        if (testDataSets.length > 0) {
          this.metaEvals$.subscribe((metaEvals: Map<string, Object>) => {
            if (metaEvals.size == testDataSets.length) {
              this.createRegularBarChart(metaEvals, 'point-pct-diffs', true);
              this.pointPctDiffChartCreated = true;
            }
          });
        }
      });
    }
  }

  createRegularBarChart(
    tdsMetaEvals: Map<string, Object>,
    evalTag: string,
    legendRequired: boolean
  ): void {
    const ROOT = d3.select('div#' + evalTag);

    if (ROOT.size() != 0) {
      // Define Constants
      const MARGIN_VERTICAL = 20;
      const MARGIN_HORIZONTAL = 20;
      const ROOT_WIDTH = parseInt(ROOT.style('width'));
      const ROOT_HEIGHT = 400;
      const SVG_WIDTH = ROOT_WIDTH - 4 * MARGIN_HORIZONTAL;
      const SVG_HEIGHT = ROOT_HEIGHT - 2 * MARGIN_VERTICAL;

      let xItems: Array<[string, number]> = [];

      if (this.averageMode) {
        Array.from(tdsMetaEvals.entries()).map(([_, tdsMetaEval]) => {
          if (Object.keys(tdsMetaEval['comparison-stats']).length > 0) {
            xItems.push([
              tdsMetaEval['student-id'],
              tdsMetaEval['comparison-stats'][evalTag][
                'latest-auto-eval' + 'avg-man-eval'
              ],
            ]);
          }
        });
      } else {
        console.warn('Not implemented!!!');
        return null;
      }

      // Define a color scale for the
      // two possible bar colors.
      let color: Map<string, string> = new Map();
      color.set('true', '#5ad16c');
      color.set('false', '#f23518');
      color.set('default', '#9e7e4a');

      let svgRoot = ROOT.append('svg')
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
        .domain(xItems.map(([studentId, _]) => studentId))
        .range([0, SVG_WIDTH])
        .padding(0.25);

      svgRoot
        .append('g')
        .style('font', '14px roboto')
        .attr(
          'transform',
          'translate(' + MARGIN_HORIZONTAL + ', ' + SVG_HEIGHT + ')'
        )
        .call(d3.axisBottom(xScale).tickSize(0).tickPadding(6));

      if (legendRequired) {
        // Append Legend
        // ~~~~~~~~~~~~~
        // Add legend container
        let legend = svgRoot
          .append('g')
          .style('font', '14px roboto')
          .attr('transform', 'translate(' + (SVG_WIDTH - 60) + ', 8)');

        // Add Legend Entry -> ManEval
        let manEntry = legend.append('g');
        manEntry
          .append('rect')
          .attr('width', 14)
          .attr('height', 14)
          .attr('fill', color.get('true'));
        manEntry
          .append('text')
          .text('Auto > Man')
          .attr('x', 22)
          .attr('y', 9)
          .attr('alignment-baseline', 'middle');

        // Add Legend Entry -> AutoEval
        let autoEntry = legend
          .append('g')
          .attr('transform', 'translate(0, 24)');
        autoEntry
          .append('rect')
          .attr('width', 14)
          .attr('height', 14)
          .attr('fill', color.get('false'));
        autoEntry
          .append('text')
          .text('Man > Auto')
          .attr('x', 22)
          .attr('y', 9)
          .attr('alignment-baseline', 'middle');
        // ~~~~~~~~~~~~~
      }

      // Define y-scale
      let yMaxValue =
        Math.max(...xItems.map(([_, evalStat]) => Math.abs(evalStat))) * 1.1;
      let yMinValue =
        Math.max(0, Math.min(...xItems.map(([_, evalStat]) => Math.abs(evalStat) * 0.8)));
      let yScale = d3
        .scaleLinear()
        .range([SVG_HEIGHT, 0])
        .domain([yMinValue, yMaxValue]);

      svgRoot
        .append('g')
        .style('font', '14px roboto')
        .attr('transform', 'translate(' + MARGIN_HORIZONTAL + ', 0)')
        .call(d3.axisLeft(yScale));

      svgRoot
        .append('g')
        .attr('transform', 'translate(' + MARGIN_HORIZONTAL + ', 0)')
        .selectAll('rect')
        .data(xItems)
        .enter()
        .append('rect')
        .attr('x', ([studentId, _]) => xScale(studentId))
        .attr('y', ([_, evalStat]) => yScale(Math.abs(evalStat)))
        .attr('height', ([_, evalStat]) => {
          return SVG_HEIGHT - yScale(Math.abs(evalStat));
        })
        .attr('width', xScale.bandwidth())
        .attr('fill', ([_, evalStat]) => {
          if (legendRequired) return color.get((evalStat > 0).toString())
          else return color.get('default');
        });
    }
  }
}
