// Copyright 2022 The DLRover Authors. All rights reserved.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package api

import pb "github.com/intelligent-machine-learning/easydl/brain/pkg/proto"

// Condition is the condition struct for read/write data
type Condition struct {
	Type    string
	JobUUID string
	Extra   interface{}
}

// DataStore interface persists job metrics into DataBase.
type DataStore interface {
	PersistMetrics(condition *Condition, jobMetrics *pb.JobMetrics, extra interface{}) error
	GetData(condition *Condition, data interface{}) error
}