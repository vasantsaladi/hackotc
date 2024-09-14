## Copyright (C) 2024 Legit
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.

## -*- texinfo -*-
## @deftypefn {} {@var{retval} =} create_forex_gui (@var{input1}, @var{input2})
##
## @seealso{}
## @end deftypefn

## Author: Christian
## Created: 2024-09-14

function create_forex_gui()
  % Create figure window
  f = figure('Position', [100, 100, 800, 600], 'MenuBar', 'none', 'Name', 'FOREX Data Visualization');

    % Create a button for loading data
    uicontrol('Style', 'pushbutton', 'String', 'Load Data', 'Position', [10, 550, 100, 30], 'Callback', @load_data);

    % Create a dropdown for selecting countries
    uicontrol('Style', 'text', 'String', 'Select Country:', 'Position', [120, 550, 100, 30]);
    global country_popup;
    country_popup = uicontrol('Style', 'popupmenu', 'String', {}, 'Position', [230, 550, 100, 30], 'Callback', @update_plot);

    % Create date range selectors
    uicontrol('Style', 'text', 'String', 'Start Date:', 'Position', [340, 550, 100, 30]);
    global start_date;
    start_date = uicontrol('Style', 'edit', 'String', 'yyyy-mm-dd', 'Position', [450, 550, 100, 30], 'Callback', @update_plot);

    uicontrol('Style', 'text', 'String', 'End Date:', 'Position', [560, 550, 100, 30]);
    global end_date;
    end_date = uicontrol('Style', 'edit', 'String', 'yyyy-mm-dd', 'Position', [670, 550, 100, 30], 'Callback', @update_plot);

    % Create axes for plotting
    global plot_axes;
    plot_axes = axes('Parent', f, 'Position', [0.1, 0.1, 0.8, 0.4]);

    % Store data in a global variable
    global forex_data;
    forex_data = [];

    function load_data(src, event)
        [file, path] = uigetfile('*.csv', 'Select FOREX Data File');
        if isequal(file, 0)
            disp('User selected Cancel');
            return;
        end
        data = csv2cell(fullfile(path, file));
        forex_data = cell2table(data(2:end, :), 'VariableNames', data(1, :));
        % Update country dropdown
        countries = unique(forex_data.Country);
        set(country_popup, 'String', countries);
        update_plot();
    end

    function update_plot(src, event)
        if isempty(forex_data)
            return;
        end
        country = get(country_popup, 'Value');
        country_name = get(country_popup, 'String'){country};
        start_date_value = get(start_date, 'String');
        end_date_value = get(end_date, 'String');

        % Filter data
        filtered_data = forex_data(strcmp(forex_data.Country, country_name) & ...
                                    forex_data.Date >= start_date_value & ...
                                    forex_data.Date <= end_date_value, :);

        % Plot data
        axes(plot_axes);
        plot(datenum(filtered_data.Date), filtered_data.Rate);
        datetick('x', 'yyyy-mm-dd', 'keepticks');
        xlabel('Date');
        ylabel('Rate');
        title(sprintf('FOREX Data for %s', country_name));

        % Save processed data to a MAT file
        save('processed_data.mat', 'filtered_data');
    end
end
