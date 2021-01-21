import { Component, Input, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { TestDataSet } from '../classes/test-data-set';
import { MetaEvalService } from '../services/metaeval.service';
import { TestDataSetService } from '../services/test-data-set-service.service';

@Component({
  selector: 'app-multiple-comparison',
  templateUrl: './multiple-comparison.component.html',
  styleUrls: ['./multiple-comparison.component.css'],
})
export class MultipleComparisonComponent implements OnInit {
  @Input()
  exerciseId: string;

  exerciseTestDataSets: TestDataSet[];

  constructor(
    public metaEvalService: MetaEvalService,
    private tdsService: TestDataSetService
  ) {}

  ngOnInit(): void {
    this.tdsService
      .getTestDataSetsOfExercise(this.exerciseId)
      .subscribe((testDataSets: TestDataSet[]) => {
        this.exerciseTestDataSets = testDataSets;
      });
  }

  ngAfterViewInit(): void {
    this.metaEvalService
      .getExerciseMetaEvals(this.exerciseId)
      .subscribe((exerciseMetaEvals: Map<string, Object>) => {
        // if the query has a body
        if (
          Array.from(exerciseMetaEvals.keys()).length ==
          this.exerciseTestDataSets.length
        ) {
          this.createGradesPerTestDataSetChart(exerciseMetaEvals);
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

      let xItems = Array.from(tdsMetaEvals.entries()).map(
        ([_, tdsMetaEvals]) => tdsMetaEvals['student-id']
      );

      let studentGrades: Map<string, Object[]> = new Map();

      // Get the relevant grades from the meta eval
      Array.from(tdsMetaEvals.entries()).map(([_, tdsMetaEval]) => {
        studentGrades.set(tdsMetaEval['student-id'], [
          { evalType: 'A', grade: tdsMetaEval['latest-auto-grade'] },
          { evalType: 'M', grade: tdsMetaEval['average-man-grade'] },
        ]);
      });

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
          return yScale(studentGrade['grade'] * 100);
        })
        .attr('height', (studentGrade) => {
          return SVG_HEIGHT - yScale(studentGrade['grade'] * 100);
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
