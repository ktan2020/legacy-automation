@Grapes([@Grab("jfree:jfreechart"), @Grab("jfree:jcommon")])

//require(groupId:'jfree', artifactId:'jfreechart', version:'1.0.5')
//require(groupId:'jfree', artifactId:'jcommon', version:'1.0.9')

import org.jfree.chart.ChartFactory
import org.jfree.chart.ChartPanel
import org.jfree.data.general.DefaultPieDataset
import groovy.swing.SwingBuilder
import java.awt.*
import javax.swing.WindowConstants as WC

def piedataset = new DefaultPieDataset();
piedataset.with {
     setValue "Apr", 10
     setValue "May", 30
     setValue "June", 40
}

def options = [true, true, true]
def chart = ChartFactory.createPieChart("Pie Chart Sample",
    piedataset, *options)
chart.backgroundPaint = Color.white
def swing = new SwingBuilder()
def frame = swing.frame(title:'Groovy PieChart',
        defaultCloseOperation:WC.EXIT_ON_CLOSE) {
    panel(id:'canvas') { widget(new ChartPanel(chart)) }
}
frame.pack()
frame.show()