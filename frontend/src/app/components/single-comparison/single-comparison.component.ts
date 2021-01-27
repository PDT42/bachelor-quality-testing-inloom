import { Component, Input, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { BehaviorSubject } from 'rxjs';
import { EvaluationService } from 'src/app/services/evaluation.service';
import { MetaEvalService } from 'src/app/services/metaeval.service';

@Component({
  selector: 'app-single-comparison',
  templateUrl: './single-comparison.component.html',
  styleUrls: ['./single-comparison.component.css'],
})
export class SingleComparisonComponent implements OnInit {
  // TODO: Rename this -> TDSComparison ?

  @Input()
  metaEval$: BehaviorSubject<Object>;
  @Input()
  manEvalKey: string;
  @Input()
  autoEvalKey: string;

  manEvalStats: Object;
  autoEvalStats: Object;

  pointsPerElementTypeCreated: boolean = false;
  pointsPerCategoryCreated: boolean = false;

  constructor(
    public metaEvalService: MetaEvalService,
    public evaluationService: EvaluationService
  ) {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.metaEval$.subscribe((metaEval: Object) => {
      if (
        Object.keys(metaEval).length > 0 &&
        !this.pointsPerElementTypeCreated
      ) {
        // Getting eval stats
        this.manEvalStats = metaEval['eval-stats'][this.manEvalKey];
        this.autoEvalStats = metaEval['eval-stats'][this.autoEvalKey];

        // Create chart
        this.createComparisonChart(
          this.manEvalStats,
          this.autoEvalStats,
          'points-per-expert-element-type'
        );
        this.pointsPerElementTypeCreated = true;
      }
    });
  }

  onTabChange(event: any) {
    if (event['index'] == 1 && !this.pointsPerCategoryCreated) {
      this.createComparisonChart(
        this.manEvalStats,
        this.autoEvalStats,
        'points-per-result-category'
      );
      this.pointsPerCategoryCreated = true;
    }
  }

  createComparisonChart(
    manEvalStats: Object,
    autoEvalStats: Object,
    chartKey: string
  ): void {
    const ROOT = d3.select('div#' + chartKey);

    if (ROOT.size() != 0) {
      const MARGIN_VERTICAL = 20;
      const MARGIN_HORIZONTAL = 20;
      const ROOT_WIDTH = parseInt(ROOT.style('width')) - MARGIN_HORIZONTAL;
      const ROOT_HEIGHT = 400;
      const SVG_WIDTH = ROOT_WIDTH - 4 * MARGIN_HORIZONTAL;
      const SVG_HEIGHT = ROOT_HEIGHT - 2 * MARGIN_VERTICAL;

      // Unpack required data
      let _autoLocalStats: Map<string, number> = autoEvalStats[chartKey];
      let _manLocalStats: Map<string, number> = manEvalStats[chartKey];

      let xItems = Array.from(
        new Set([
          ...Object.keys(_manLocalStats),
          ...Object.keys(_autoLocalStats),
        ])
      );
      let yMaxValue = d3.max(
        new Set<number>([
          ...Object.values(_manLocalStats),
          ...Object.values(_autoLocalStats),
        ])
      );

      let xCategoryStats: Map<string, Object[]> = new Map();

      for (let xCategory of xItems) {
        let manPoints: number = _manLocalStats[xCategory];
        let autoPoints: number = _autoLocalStats[xCategory];

        if (!manPoints) manPoints = 0;
        if (!autoPoints) autoPoints = 0;

        xCategoryStats.set(xCategory, [
          { xCategory: 'A', points: autoPoints },
          { xCategory: 'M', points: manPoints },
        ]);
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
        .padding(0.3);

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
        .padding(0.1);

      // Define y-scale
      let yScale = d3
        .scaleLinear()
        .range([SVG_HEIGHT, 0])
        .domain([0, yMaxValue * 1.1]);

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
        .attr('transform', (xCategory) => {
          return 'translate(' + xScale(xCategory) + ')';
        })
        .selectAll('rect')
        .data((xCategory) => {
          return xCategoryStats.get(xCategory);
        })
        .enter()
        .append('rect')
        .attr('x', (xCategoryStats) => {
          return xSubScale(xCategoryStats['xCategory']);
        })
        .attr('y', (xCategoryStats) => {
          return yScale(xCategoryStats['points']);
        })
        .attr('height', (xCategoryStats) => {
          return SVG_HEIGHT - yScale(xCategoryStats['points']);
        })
        .attr('width', xSubScale.bandwidth())
        .attr('fill', (xCategoryStats): string => {
          if (xCategoryStats['xCategory'] != null) {
            return color.get(xCategoryStats['xCategory']);
          } else return null;
        });
    }
  }
}
