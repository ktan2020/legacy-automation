    class DijkstrasShortestPathAlgoritm {  
        def graph, start, destination      
        // PriorityQueue performs much better than List - O(log(n)) for poll.      
        def unsettledNodes = new PriorityQueue<String>(100, new Comparator<String>() {  
           public int compare(String node1, String node2) {  
                shortestDistance(node1).compareTo(shortestDistance(node2))  
            }  
        });  
        def shortestDistances = [:]  
        def predecessors = [:]  
        def settledNodes = [] as Set  
      
        DijkstrasShortestPathAlgoritm(graph, start, destination) {  
            this.graph = graph  
            this.start = start  
            this.destination = destination  
      
            unsettledNodes.add(start)  
            shortestDistances[(start)] = 0  
        }  
      
        int shortestDistance(node) {  
            shortestDistances.containsKey(node) ? shortestDistances[node] : Integer.MAX_VALUE  
        }  
      
        def extractMin() {  
            unsettledNodes.poll()  
        }  
      
        def unsettledNeighbours(node) {  
            graph.findAll { edge ->  
                edge.node1 == node && !settledNodes.contains(edge.node2)  
            }  
        }  
      
        def relaxNeighbours(node) {  
            unsettledNeighbours(node).each { edge ->  
                if (shortestDistance(edge.node2) > shortestDistance(edge.node1) + edge.distance) {  
                    shortestDistances[edge.node2] = shortestDistance(edge.node1) + edge.distance  
                    predecessors[edge.node2] = edge.node1  
                    if (!unsettledNodes.contains(edge.node2)) {  
                        unsettledNodes.add(edge.node2)  
                    }  
                }  
            }  
        }  
      
        def calculateShortestPath() {  
            while (!unsettledNodes.isEmpty()) {  
                String node = extractMin()  
                if (node == destination) {  
                    break  
                }  
                settledNodes += node  
                relaxNeighbours(node)  
            }  
            shortestDistances[destination]  
        }  
      
        private def getShortestPath(node, path) {  
            node == start ? [node]+path : getShortestPath(predecessors[node], [node]+path)  
        }  
          
        def getShortestPath() {  
            getShortestPath(destination, [])   
        }  
    }  
	
	class Edge {  
	String node1, node2  
	int distance  
    }  
    graph = [  
        new Edge(node1:'a', node2:'b', distance:4),  
        new Edge(node1:'a', node2:'c', distance:2),  
        new Edge(node1:'b', node2:'c', distance:3),  
        new Edge(node1:'c', node2:'b', distance:1),  
        new Edge(node1:'c', node2:'d', distance:5),  
        new Edge(node1:'b', node2:'d', distance:1),  
        new Edge(node1:'a', node2:'e', distance:1),  
        new Edge(node1:'e', node2:'d', distance:4)  
    ]  
    def dijkstra = new DijkstrasShortestPathAlgoritm(graph, 'a', 'd')  
    d = dijkstra.calculateShortestPath();  
    assert d == 4  
    assert dijkstra.shortestPath == ['a','c','b','d']  
