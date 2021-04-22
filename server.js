// To get the interface is node server.js and access it at (http://localhost:4000/graphql)
// In the interface you can use the commands below to get result:

// {
//     othercall
// }

// {
//     usercall(id: 'a') {
//         id
//         name
//     }
// }

var express = require('express')
var { graphqlHTTP } = require('express-graphql')
var { buildSchema } = require('graphql')

var schema = buildSchema(`
  type User {
    id: String
    name: String
  }

  type Student {
    studentId: String
    studentName: String
    studentDOB: String
  }

  type Query {
    usercall(id: String): User
    queryById(studentId: String): Student
    queryByName(studentName: String): Student
    queryByDOB(studentDOB: String): Student
    othercall:String
  }
`);

// Map ID to user objects
var userDB = {
    'a' : {
        id: 'a',
        name: 'alice'
    },
    'b' : {
        id: 'b',
        name: 'bob'
    },
    'c' : {
        id: 'c',
        name: 'carl'
    }
};

// Map ID to user objects
var studentDB = {
    '1' : {
        studentId: 'B0010',
        studentName: 'alice',
        studentDOB: '121120'
    },
    '2' : {
        studentId: 'B0020',
        studentName: 'bob',
        studentDOB: '031298'
    },
    '3' : {
        studentId: 'B0030',
        studentName: 'carl',
        studentDOB: '010199'
    },
    '4' : {
        studentId: 'B0040',
        studentName: 'jess',
        studentDOB: '150997'
    },
    '5' : {
        studentId: 'B0050',
        studentName: 'kai',
        studentDOB: '201199'
    }
};

var root = {
    usercall: ({id}) => {
        return userDB[id];
    },

    queryById: ({studentId}) => {
        if (studentId == 'B0010') {
            return studentDB['1']
        }

        if (studentId == 'B0020') {
            return studentDB['2']
        }

        if (studentId == 'B0030') {
            return studentDB['3']
        }

        if (studentId == 'B0040') {
            return studentDB['4']
        }

        if (studentId == 'B0050') {
            return studentDB['5']
        }
    },

    queryByName: ({studentName}) => {
        if (studentName == 'alice') {
            return studentDB['1']
        }

        if (studentName == 'bob') {
            return studentDB['2']
        }

        if (studentName == 'carl') {
            return studentDB['3']
        }

        if (studentName == 'jess') {
            return studentDB['4']
        }

        if (studentName == 'kai') {
            return studentDB['5']
        }
    },

    queryByDOB: ({studentDOB}) => {
        if (studentDOB == '121120') {
            return studentDB['1']
        }

        if (studentDOB == '031298') {
            return studentDB['2']
        }

        if (studentDOB == '010199') {
            return studentDB['3']
        }

        if (studentDOB == '150997') {
            return studentDB['4']
        }

        if (studentDOB == '201199') {
            return studentDB['5']
        }
    },

    othercall: ({}) => {
        return 'This is the other call'
    }
};

var app = express();
app.use('/graphql', graphqlHTTP({
    schema: schema,
    rootValue: root,
    graphiql: true,
}));
app.listen(4000);
console.log('Running a GraphQL API server at localhost:4000/graphql')