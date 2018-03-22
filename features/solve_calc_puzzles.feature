# Created by rony at 3/21/18
Feature: Solve "calculator - the game puzzles"
  Solve puzzles form the game

  Scenario Outline: Simple case
    Given The starting number is <start>
    And the valid operations are <operations>
    And the goal is <goal>
    And I have <steps> steps available
    When I solve the puzzle
    Then The solution steps must be <solution>

    Examples:
      | start | goal | steps | operations | solution       |
      | 0     | 2    | 5     | +4 x9 <<   | +4 x9 << x9 << |
      | 0     | 210  | 5     | +5 -5 5 2  | 2 5 -5 5 +5    |
      | 171   | 23   | 4     | x2 -9 <<   | -9 x2 << -9    |
      | 0     | 1    | 1     | +1         | +1             |
      | 0     | 2    | 2     | +1         | +1 +1          |
      | 0     | 8    | 3     | +2 +3      | +2 +3 +3       |
      | 0     | 222  | 4     | 1 1=>2     | 1 1 1 1=>2     |
      | 111   | 222  | 1     | 1=>2       | 1=>2           |
      | 40    | 2020 | 4     | 0 +4 /2    | 0 +4 0 /2      |
      | 0     | 11   | 4     | 12 <<      | 12 << 12 <<    |
      | 0     | 102  | 4     | 10 +1 <<   | 10 10 << +1    |
      | 0     | 222  | 4     | 1 1=>2     | 1 1 1 1=>2     |


  Scenario Outline: Parse operations
    When I try to parse the step <step>
    Then I should have the parsed operation <literal>
    Examples:
      | step | literal                  |
      | 0    | NumberOperation('0')     |
      | 1    | NumberOperation('1')     |
      | 2    | NumberOperation('2')     |
      | 3    | NumberOperation('3')     |
      | 171  | NumberOperation('171')   |
      | +4   | AddOperation('4')        |
      | -9   | DiffOperation('9')       |
      | x2   | MultiplyOperation('2')   |
      | x9   | MultiplyOperation('9')   |
      | /4   | DivideOperation('4')     |
      | <<   | DeleteOperation()        |
      | 1=>2 | ConvertNumOperation(1,2) |
